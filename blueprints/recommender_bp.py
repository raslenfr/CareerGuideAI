"""
POST /api/recommender/start
    ➤ Initiates job recommendation process based on keywords & location.

Request:
{
    "keywords": "Python Developer",
    "location": "Bangalore"
}

Response:
{
    "success": true,
    "job_count": 4,
    "questions": [
        {"id": "q_skill_python", "text": "Rate your experience with Python..."},
        ...
    ],
    "request_id": "uuid-1234"
}

POST /api/recommender/submit
    ➤ Submits answers to questions and returns job recommendations.

Request:
{
    "request_id": "uuid-1234",
    "answers": {
        "q_skill_python": "5",
        "q_interest_data": "4"
    }
}

Response:
{
    "success": true,
    "recommendations": [
        {
            "title": "Data Scientist",
            "company": "HealthAnalytics AI",
            "match_score": 0.87,
            "reason": "Strong Python and data interest..."
        },
        ...
    ]
}
"""

from flask import Blueprint, request, jsonify
from services.job_search_service import search_online_jobs # Using static data
from services.llm_service import analyze_jobs_and_generate_questions, get_job_recommendations
import time
import logging
import uuid # Use UUID for request IDs

log = logging.getLogger(__name__)

recommender_bp = Blueprint('recommender_bp', __name__, url_prefix='/api/recommender')

# Simple in-memory cache
# WARNING: Not suitable for multi-process/multi-user production environments. Use Redis/DB instead.
recommendation_cache = {}
CACHE_TTL_SECONDS = 600 # 10 minutes

def _clean_expired_cache():
    current_time = time.time()
    expired_keys = [k for k, v in recommendation_cache.items() if current_time - v.get('timestamp', 0) > CACHE_TTL_SECONDS]
    if expired_keys:
         log.info(f"Removing {len(expired_keys)} expired cache entries.")
         for k in expired_keys: recommendation_cache.pop(k, None)

@recommender_bp.route('/start', methods=['POST'])
def start_recommendation():
    """Starts recommendation: fetches jobs, generates survey questions."""
    _clean_expired_cache()

    data = request.get_json()
    keywords = data.get('keywords', '') if isinstance(data, dict) else ''
    location = data.get('location', 'Tunisia') if isinstance(data, dict) else 'Tunisia'

    if not isinstance(keywords, str) or len(keywords) > 150:
         log.warning(f"Recommender start validation failed: Invalid 'keywords'. Length: {len(keywords)}")
         return jsonify({"success": False, "error": "Invalid 'keywords' (string, max 150 chars)"}), 400
    if not isinstance(location, str) or len(location) > 100:
         log.warning(f"Recommender start validation failed: Invalid 'location'. Length: {len(location)}")
         return jsonify({"success": False, "error": "Invalid 'location' (string, max 100 chars)"}), 400

    request_id = str(uuid.uuid4()) # Generate unique ID for this request
    log.info(f"Starting recommendation request ID: {request_id}")

    # Step 1: Search (Static)
    found_jobs = search_online_jobs(keywords, location)
    if not found_jobs:
        log.info(f"Request ID {request_id}: No relevant static jobs found for keywords '{keywords}'.")
        # Still return success=True but indicate no jobs found
        return jsonify({"success": True, "message": "No relevant jobs found (using static data).", "questions": [], "request_id": request_id, "job_count": 0})

    # Step 2: Generate Questions (Static questions in this version)
    q_response = analyze_jobs_and_generate_questions(found_jobs)
    survey_questions = q_response.get('questions', [])
    if not q_response['success'] or not survey_questions:
         log.error(f"Request ID {request_id}: Failed to generate survey questions.")
         return jsonify({"success": False, "error": "Internal error: Failed to prepare survey questions."}), 500

    # Cache data needed for the submit step
    recommendation_cache[request_id] = {
        'jobs': found_jobs,
        'questions': survey_questions, # Store questions asked
        'timestamp': time.time()
    }
    log.info(f"Request ID {request_id}: Cached {len(found_jobs)} jobs and {len(survey_questions)} questions.")

    return jsonify({
        "success": True,
        "message": f"Found {len(found_jobs)} potential jobs (static data). Please answer the questions below.",
        "job_count": len(found_jobs),
        "questions": survey_questions,
        "request_id": request_id # Client needs this for the submit step
    })

@recommender_bp.route('/submit', methods=['POST'])
def submit_survey():
    """Receives survey answers and returns job recommendations."""
    _clean_expired_cache()

    data = request.get_json()
    if not data or not isinstance(data, dict):
        log.warning("Recommender submit request body is missing or not JSON")
        return jsonify({"success": False, "error": "Invalid request body. JSON object expected."}), 400
    request_id = data.get('request_id')
    answers = data.get('answers')

    # Validation
    if not request_id or not isinstance(request_id, str):
        log.warning(f"Recommender submit validation failed: Missing or invalid 'request_id'. Received: {request_id}")
        return jsonify({"success": False, "error": "Missing or invalid 'request_id'"}), 400
    if not answers or not isinstance(answers, dict):
        log.warning(f"Recommender submit validation failed: Missing or invalid 'answers'. Received type: {type(answers)}")
        return jsonify({"success": False, "error": "Missing or invalid 'answers' (must be a dictionary/object)"}), 400

    # Retrieve cached data
    cached_data = recommendation_cache.get(request_id)
    if not cached_data:
        log.warning(f"Recommender submit: Invalid or expired request_id '{request_id}'. Cache keys: {list(recommendation_cache.keys())}")
        return jsonify({"success": False, "recommendations": None, "error": "Invalid or expired request session ID. Please start the recommendation process again."}), 400 # 400 Bad Request seems appropriate

    # Optional: Validate answers against cached questions
    cached_questions = cached_data.get('questions', [])
    question_ids = {q['id'] for q in cached_questions}
    if not all(qid in question_ids for qid in answers.keys()):
         log.warning(f"Request ID {request_id}: Submitted answers contain keys not present in the cached questions.")
         # Decide whether to reject or proceed cautiously
         # return jsonify({"success": False, "error": "Submitted answers do not match the questions asked."}), 400

    log.info(f"Request ID {request_id}: Received survey answers. Starting recommendation generation.")
    found_jobs = cached_data['jobs']

    # Step 3: Get Recommendations (using refined service)
    response_data = get_job_recommendations(found_jobs, answers)

    # Clean up this specific entry from cache after use
    recommendation_cache.pop(request_id, None)
    log.info(f"Request ID {request_id}: Removed from cache after processing.")

    if response_data['success']:
        recs = response_data['recommendations']
        log.info(f"Request ID {request_id}: Generated {len(recs)} job recommendations successfully.")
        return jsonify({
            "success": True,
            "recommendations": recs,
            "message": f"Based on your answers, here are the top {len(recs)} job recommendations."
        })
    else:
        log.error(f"Request ID {request_id}: Failed during recommendation generation. Error: {response_data['error']}")
        status_code = 500
        if "client not initialized" in response_data.get('error', ''): status_code = 503
        elif "Rate Limit Error" in response_data.get('error', ''): status_code = 429
        return jsonify({"success": False, "recommendations": None, "error": response_data['error']}), status_code
