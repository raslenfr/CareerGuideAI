"""
GET /api/suggester/start
    ➤ Returns the first question in the static Q&A career survey.

POST /api/suggester/answer
    ➤ Accepts an answer and returns the next question or final suggestions.

Request Body:
{
    "answer": "I love problem-solving and coding",
    "current_question_index": 0,
    "answers_so_far": {}
}

Response (final):
{
    "success": true,
    "suggestions": {
        "summary": "You enjoy analytical problem solving...",
        "suggestions": [
            {"career": "Software Engineer", "reason": "Your love for coding..."},
            ...
        ]
    },
    "final_answers": {...},
    "next_question": null
}
"""

from flask import Blueprint, request, jsonify
from services.llm_service import get_career_suggestions_from_answers
from extensions import db
from models import CareerSuggestion
import logging
import json
import uuid

log = logging.getLogger(__name__)
suggester_bp = Blueprint('suggester_bp', __name__, url_prefix='/api/suggester')

# ✅ Improved Static Questions (11 total)
QUESTIONS = [
    {"id": "q1", "text": "What subjects or activities did you enjoy most in school/university, and why?"},
    {"id": "q2", "text": "What are 2-3 of your strongest skills (e.g., communication, problem-solving, specific software, technical skills)?"},
    {"id": "q3", "text": "Describe your ideal work environment (e.g., collaborative team, independent work, fast-paced, structured, creative)."},
    {"id": "q4", "text": "What kind of problems or challenges do you find motivating or enjoyable to tackle?"},
    {"id": "q5", "text": "What are your salary expectations or financial goals for your career (optional)?"},
    {"id": "q6", "text": "Are there any industries or types of companies you are particularly interested in or want to avoid?"},
    # New Questions:
    {"id": "q7", "text": "What is your current level of education (e.g., 12th, UG, PG, Diploma, PhD)?"},
    {"id": "q8", "text": "Have you done any internships or projects? If yes, briefly describe them."},
    {"id": "q9", "text": "Do you have any certifications or courses completed (e.g., AWS, Python, Marketing, etc.)?"},
    {"id": "q10", "text": "Would you prefer a technical, managerial, creative, research-oriented, or people-facing role?"},
    {"id": "q11", "text": "Are you open to relocation or do you prefer working in a specific city or region?"},
]

@suggester_bp.route('/start', methods=['GET'])
def start_suggestion():
    if not QUESTIONS:
        log.error("Suggester questions list is empty.")
        return jsonify({"success": False, "error": "No questions defined."}), 500
    return jsonify({
        "success": True,
        "next_question": QUESTIONS[0],
        "answers_so_far": {},
        "current_question_index": 0
    })

@suggester_bp.route('/answer', methods=['POST'])
def handle_answer():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Invalid JSON body."}), 400

    required_keys = ['answer', 'current_question_index', 'answers_so_far']
    if not all(key in data for key in required_keys):
        return jsonify({"success": False, "error": "Missing required fields."}), 400

    answer = data['answer']
    index = data['current_question_index']
    answers = data['answers_so_far']

    if not isinstance(answer, str) or len(answer.strip()) == 0 or len(answer) > 1500:
        return jsonify({"success": False, "error": "Invalid answer (must be 1–1500 characters)."}), 400

    if not isinstance(index, int) or index < 0 or index >= len(QUESTIONS):
        return jsonify({"success": False, "error": "Invalid question index."}), 400

    question_text = QUESTIONS[index]['text']
    answers[question_text] = answer.strip()

    next_index = index + 1
    if next_index < len(QUESTIONS):
        return jsonify({
            "success": True,
            "next_question": QUESTIONS[next_index],
            "answers_so_far": answers,
            "current_question_index": next_index
        })

    # All questions answered → call LLM
    log.info("All questions answered. Sending to LLM.")
    response_data = get_career_suggestions_from_answers(answers)
    if response_data['success']:
        return jsonify({
            "success": True,
            "suggestions": response_data['data'],
            "final_answers": answers,
            "next_question": None
        })
    else:
        return jsonify({
            "success": False,
            "error": response_data['error'],
            "raw_content_debug": response_data.get('raw_content', '')
        }), 500


def generate_session_title(answers):
    """Generate a title for the suggestion session based on the user's answers."""
    # Try to use their education level and career preference
    title_parts = []
    
    for question, answer in answers.items():
        if 'education' in question.lower() and answer:
            title_parts.append(answer.split(',')[0][:30])
        elif 'prefer' in question.lower() and 'role' in question.lower() and answer:
            title_parts.append(answer.split(',')[0][:30])
    
    if title_parts:
        return f"{' - '.join(title_parts[:2])}"
    
    # Fallback: use first answer or generic title
    first_answer = list(answers.values())[0] if answers else ""
    return first_answer[:50] if first_answer else "Career Suggestion Session"


@suggester_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save a career suggestion session to the database."""
    data = request.get_json()
    
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Invalid request body"}), 400
    
    user_id = data.get('user_id')
    answers = data.get('answers')
    suggestions = data.get('suggestions')
    session_id = data.get('session_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id is required"}), 400
    
    if not answers or not isinstance(answers, dict):
        return jsonify({"success": False, "error": "answers must be provided as an object"}), 400
    
    if not suggestions or not isinstance(suggestions, dict):
        return jsonify({"success": False, "error": "suggestions must be provided as an object"}), 400
    
    try:
        # Generate session_id if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Check if session already exists
        existing = CareerSuggestion.query.filter_by(user_id=user_id, session_id=session_id).first()
        if existing:
            return jsonify({"success": False, "error": "Session already saved"}), 400
        
        # Generate session title
        session_title = generate_session_title(answers)
        
        # Create new suggestion session
        new_session = CareerSuggestion(
            user_id=user_id,
            session_id=session_id,
            session_title=session_title,
            answers=json.dumps(answers),
            suggestions=json.dumps(suggestions)
        )
        
        db.session.add(new_session)
        db.session.commit()
        
        log.info(f"Career suggestion session saved successfully for user {user_id}, session {session_id}")
        
        return jsonify({
            "success": True,
            "message": "Session saved successfully",
            "session_id": session_id,
            "session_title": session_title
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.error(f"Error saving suggestion session: {str(e)}")
        return jsonify({"success": False, "error": "Failed to save session"}), 500


@suggester_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all suggestion sessions for a user."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id is required"}), 400
    
    try:
        sessions = CareerSuggestion.query.filter_by(user_id=user_id).order_by(CareerSuggestion.created_at.desc()).all()
        
        sessions_list = []
        for session in sessions:
            sessions_list.append({
                'id': session.id,
                'session_id': session.session_id,
                'session_title': session.session_title,
                'created_at': session.created_at.isoformat() if session.created_at else None
            })
        
        return jsonify({
            "success": True,
            "sessions": sessions_list
        }), 200
        
    except Exception as e:
        log.error(f"Error fetching suggestion sessions: {str(e)}")
        return jsonify({"success": False, "error": "Failed to fetch sessions"}), 500


@suggester_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific suggestion session by session_id."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id is required"}), 400
    
    try:
        session = CareerSuggestion.query.filter_by(user_id=user_id, session_id=session_id).first()
        
        if not session:
            return jsonify({"success": False, "error": "Session not found"}), 404
        
        return jsonify({
            "success": True,
            "session": session.to_dict()
        }), 200
        
    except Exception as e:
        log.error(f"Error fetching session {session_id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to fetch session"}), 500


@suggester_bp.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a suggestion session."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id is required"}), 400
    
    try:
        session = CareerSuggestion.query.filter_by(user_id=user_id, session_id=session_id).first()
        
        if not session:
            return jsonify({"success": False, "error": "Session not found"}), 404
        
        db.session.delete(session)
        db.session.commit()
        
        log.info(f"Suggestion session {session_id} deleted successfully")
        
        return jsonify({
            "success": True,
            "message": "Session deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.error(f"Error deleting session {session_id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to delete session"}), 500
