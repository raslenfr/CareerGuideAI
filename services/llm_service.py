"""
Functions:
- get_career_advice(user_message, history)
- get_career_suggestions_from_answers(answers)
- analyze_jobs_and_generate_questions(job_listings)
- get_job_recommendations(job_listings, answers)

All interact with Groq LLM for intelligent text or structured responses.
"""
import os
import json
import time
from groq import Groq, APIError, RateLimitError, APIConnectionError
from dotenv import load_dotenv
import logging

# Configure logging (Ensure this runs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s')
log = logging.getLogger(__name__) # Use named logger

load_dotenv()

# --- Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    log.critical("GROQ_API_KEY environment variable not set. LLM service will not function.")

# Centralized Model Definitions
# Updated to current Groq models (llama3-70b-8192 was decommissioned)
MODEL_CHAT = "llama-3.3-70b-versatile"
MODEL_SUGGEST = "llama-3.3-70b-versatile"
MODEL_ANALYZE = "llama-3.3-70b-versatile"

# --- Groq Client Initialization ---
try:
    if GROQ_API_KEY:
         client = Groq(api_key=GROQ_API_KEY, timeout=30.0)
         log.info("Groq client initialized successfully.")
    else:
         client = None
         log.warning("Groq client not initialized due to missing API key.")
except Exception as e:
    log.critical(f"Failed to initialize Groq client: {e}")
    client = None

# --- Core LLM Interaction Function ---
def ask_llm(
    messages: list,
    model: str = MODEL_CHAT,
    temperature: float = 0.7,
    max_retries: int = 1,
    json_mode: bool = False
) -> dict:
    """Sends messages to the Groq LLM, handles errors, retries, and JSON parsing."""
    if not client:
        log.error("Attempted to call ask_llm, but Groq client is not initialized.")
        return {'success': False, 'content': None, 'error': "Groq client not initialized."}

    retry_count = 0
    while retry_count <= max_retries:
        try:
            completion_params = {
                "messages": [msg.copy() for msg in messages], # Use a copy
                "model": model,
                "temperature": temperature,
            }
            _messages_for_call = completion_params["messages"]
            if json_mode and _messages_for_call:
                json_instruction = "\n\nCRITICAL INSTRUCTION: Your response MUST be ONLY a single, valid JSON object conforming to the structure requested in the prompt. Do not include any introductory text, explanations, apologies, or markdown formatting like ```json ... ```."
                system_message_index = next((i for i, msg in enumerate(_messages_for_call) if msg["role"] == "system"), -1)
                if system_message_index != -1: 
                    _messages_for_call[system_message_index]["content"] += json_instruction
                else: 
                    _messages_for_call.insert(0, {"role": "system", "content": json_instruction.strip()})

            start_time = time.time()
            log.info(f"Sending request to Groq (Model: {model}, Temp: {temperature}, JSON Mode: {json_mode}, Attempt: {retry_count+1})")
            chat_completion = client.chat.completions.create(**completion_params)
            duration = time.time() - start_time
            log.info(f"Groq API call successful in {duration:.2f} seconds.")

            raw_content = chat_completion.choices[0].message.content

            if json_mode:
                try:
                    log.debug(f"Attempting to parse JSON from raw response: {raw_content[:500]}...")
                    cleaned_content = raw_content.strip()
                    if cleaned_content.startswith("```json"): 
                        cleaned_content = cleaned_content[7:]
                    if cleaned_content.endswith("```"): 
                        cleaned_content = cleaned_content[:-3]
                    cleaned_content = cleaned_content.strip()

                    parsed_json = json.loads(cleaned_content)
                    log.debug("Successfully parsed LLM response as JSON.")
                    return {'success': True, 'content': parsed_json, 'error': None}
                except json.JSONDecodeError as json_err:
                    error_msg = f"LLM response was not valid JSON after cleaning: {json_err}"
                    log.warning(f"{error_msg}. Raw content snippet: {raw_content[:500]}...")
                    return {'success': False, 'content': raw_content, 'error': error_msg}
            else:
                return {'success': True, 'content': raw_content, 'error': None}

        except RateLimitError as e:
            error_message = f"Groq API Rate Limit Error: {e}"
            log.error(error_message)
            return {'success': False, 'content': None, 'error': error_message}
        except APIConnectionError as e:
            error_message = f"Groq API Connection Error: {e}"
            log.warning(f"{error_message}. Retrying ({retry_count+1}/{max_retries})...")
            retry_count += 1
            if retry_count > max_retries: 
                return {'success': False, 'content': None, 'error': f"{error_message} (Max retries exceeded)"}
            time.sleep(1.5 ** retry_count)
        except APIError as e:
            error_message = f"Groq API Error (Status: {e.status_code}): {e.message}"
            log.error(error_message)
            if e.status_code >= 500 and retry_count < max_retries:
                 log.warning(f"Retrying APIError ({retry_count+1}/{max_retries})...")
                 retry_count += 1
                 time.sleep(1.5 ** retry_count)
            else: 
                return {'success': False, 'content': None, 'error': error_message}
        except Exception as e:
            error_message = f"Unexpected error during Groq API call: {e.__class__.__name__}: {e}"
            log.exception(error_message)
            return {'success': False, 'content': None, 'error': "An unexpected server error occurred during LLM interaction."}

    return {'success': False, 'content': None, 'error': "LLM call failed after retries."}

# --- Specific Use Case Functions ---
def get_career_advice(user_message: str, history: list = None) -> dict:
    system_prompt = """
    You are Raslen Ferchichi, a highly experienced, empathetic, and professional AI Career Guidance Counselor with deep knowledge of the current global job market as of 2025. 

    Your mission is to provide users with clear, practical, and encouraging career advice tailored to their unique questions and situations. 

    Always communicate with warmth and understanding, making users feel supported and motivated.

    If a user's question is vague or incomplete, proactively ask specific, thoughtful clarifying questions to better understand their needs before providing advice.

    Keep your responses concise and focused — ideally 2 to 4 paragraphs — with actionable steps, useful resources, and realistic guidance.

    Never fabricate job market data or statistics. Instead, rely on widely accepted facts or guide users toward trusted sources.

    Maintain the conversational context provided in the history to ensure continuity and relevance.

    Where appropriate, suggest next steps such as skill-building, networking, or exploring specific career fields.

    Use clear, jargon-free language accessible to a broad audience.
    """
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        processed_history = []
        for entry in history[-8:]:
            if entry.get("role") in ["user", "assistant"] and entry.get("content"):
                processed_history.append({"role": entry["role"], "content": entry["content"]})
        messages.extend(processed_history)
    messages.append({"role": "user", "content": user_message})
    response_data = ask_llm(messages, model=MODEL_CHAT, temperature=0.65, json_mode=False)
    if response_data['success']:
        log.info("Career advice generated successfully.")
        return {'success': True, 'reply': response_data['content'], 'error': None}
    else:
        log.error(f"Failed to get career advice: {response_data['error']}")
        return {'success': False, 'reply': None, 'error': response_data['error']}

def get_career_suggestions_from_answers(answers: dict) -> dict:
    """Analyzes Q&A answers and suggests careers (structured JSON response)."""
    system_prompt = """You are an expert Career Suggester focusing on opportunities within Tunisia (as of April 2025).
Analyze the user's answers provided below. Based SOLELY on these answers, suggest 3 to 5 relevant career paths available in Tunisia.
Your response MUST be a single, valid JSON object containing exactly two keys:

suggestions: A JSON list (array). Each element must be a JSON object with exactly two string keys: career (the path name) and reason (concise justification based on answers).

summary: A brief (1-3 sentences) textual summary of the user's profile derived from their answers."""
    prompt_content = "Analyze the following User Answers to generate career suggestions:\n"
    for q, a in answers.items(): 
        prompt_content += f'- "{q}": "{a[:500]}"\n'
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt_content}]
    response_data = ask_llm(messages, model=MODEL_SUGGEST, temperature=0.25, json_mode=True)
    if response_data['success'] and isinstance(response_data['content'], dict):
        content = response_data['content']
        if 'suggestions' in content and 'summary' in content and isinstance(content['suggestions'], list):
            valid_suggestions = all(isinstance(item, dict) and 'career' in item and 'reason' in item for item in content['suggestions'])
            if valid_suggestions:
                log.info("Career suggestions generated and parsed successfully.")
                return {'success': True, 'data': content, 'error': None}
            else: 
                error_msg = "LLM response JSON has incorrect structure within 'suggestions' list."
        else: 
            error_msg = "LLM response JSON is missing required keys ('suggestions', 'summary') or 'suggestions' is not a list."
        log.warning(f"{error_msg}. Raw content: {response_data['content']}")
        return {'success': False, 'data': None, 'error': error_msg, 'raw_content': response_data['content']}
    elif response_data['success']:
        error_msg = response_data.get('error', 'Failed to parse LLM response as JSON dict.')
        log.warning(f"Career suggestion LLM call succeeded but response wasn't expected dict. Error: {error_msg}")
        return {'success': False, 'data': None, 'error': error_msg, 'raw_content': response_data['content']}
    else:
        log.error(f"Failed to get career suggestions: {response_data['error']}")
        return {'success': False, 'data': None, 'error': response_data['error']}

def analyze_jobs_and_generate_questions(job_listings: list) -> dict:
    """Generates static survey questions."""
    log.info("Generating static questions for job recommender.")
    static_questions = [
        {"id": "q_skill_python", "text": "Rate your experience level with Python (1=None, 3=Familiar, 5=Expert):"},
        {"id": "q_skill_frontend", "text": "How comfortable are you with modern frontend frameworks like React/Vue? (1=Not at all, 3=Somewhat, 5=Very)"},
        {"id": "q_skill_cloud", "text": "Do you have hands-on experience with cloud platforms like AWS, Azure, or GCP? (Yes/No/Learning)"},
        {"id": "q_interest_data", "text": "How interested are you in working with data analysis or machine learning? (1=Low, 3=Medium, 5=High)"},
        {"id": "q_preference_role", "text": "Do you prefer Backend, Frontend, Full Stack, DevOps/Cloud, Data Science, or non-technical roles (e.g., Marketing, Research)?"},
        {"id": "q_preference_work_mode", "text": "What is your preferred work mode? (Remote/Hybrid/Office)"},
        {"id": "q_preference_company_type", "text": "Do you prefer working in Startups, Mid-sized companies, or Large enterprises?"}
    ]
    return {'success': True, 'questions': static_questions, 'error': None}

def get_job_recommendations(job_listings: list, survey_answers: dict) -> dict:
    """Matches survey answers to static job listings, using LLM for match reasoning (JSON output)."""
    potential_matches = []
    log.info(f"Performing basic scoring for {len(job_listings)} static jobs based on survey answers.")
    for job in job_listings:
        score = 0.5
        reasons = []
        try:
            # --- Detailed matching logic ---
            skills = job.get('skills','').lower()
            tags = [t.lower() for t in job.get('tags', [])]
            title = job.get('title', '').lower()
            location = job.get('location', '').lower()

            if 'q_skill_python' in survey_answers and ('python' in skills or 'backend' in tags or 'full stack' in tags or 'data science' in tags): 
                score += (int(survey_answers['q_skill_python']) - 1) * 0.05
            if 'q_skill_frontend' in survey_answers and ('react' in skills or 'frontend' in tags or 'full stack' in tags or 'javascript' in skills): 
                score += (int(survey_answers['q_skill_frontend']) - 1) * 0.04
            if survey_answers.get('q_skill_cloud','').lower() == 'yes' and ('cloud' in tags or 'aws' in skills or 'devops' in tags): 
                score += 0.15
            if 'q_interest_data' in survey_answers and ('data science' in tags or 'ml' in tags or 'analytics' in skills): 
                score += (int(survey_answers['q_interest_data']) - 1) * 0.03
            if 'q_preference_role' in survey_answers:
                pref_role = survey_answers['q_preference_role'].lower()
                job_keywords = tags + title.split() + skills.split(',')
                if any(keyword in pref_role for keyword in job_keywords if keyword in ['backend', 'frontend', 'full stack', 'devops', 'cloud', 'data science', 'marketing', 'research', 'java', 'python', 'developer']): 
                    score += 0.12
            if 'q_preference_work_mode' in survey_answers:
                pref_mode = survey_answers['q_preference_work_mode'].lower()
                if pref_mode == 'remote' and ('remote' in location or 'remote' in tags): 
                    score += 0.1
                elif pref_mode == 'hybrid' and ('hybrid' in location or 'hybrid' in tags): 
                    score += 0.1
                elif pref_mode == 'office' and not any(m in location or m in tags for m in ['remote', 'hybrid']): 
                    score += 0.05
            if 'q_preference_company_type' in survey_answers:
                pref_comp = survey_answers['q_preference_company_type'].lower()
                if 'startup' in pref_comp and 'startup' in tags: 
                    score += 0.08
                elif ('large' in pref_comp or 'enterprise' in pref_comp) and 'enterprise' in tags: 
                    score += 0.08
        except Exception as e: 
            log.warning(f"Error during basic scoring for job {job.get('id')}: {e}")
        job['calculated_score'] = min(max(score, 0.0), 1.0)
        potential_matches.append(job)

    potential_matches.sort(key=lambda x: x.get('calculated_score', 0.0), reverse=True)
    top_n_for_llm = 7
    top_matches = potential_matches[:top_n_for_llm]
    log.info(f"Selected top {len(top_matches)} jobs after basic scoring for LLM reasoning.")

    if top_matches:
        system_prompt_match = """You are an AI Job Match Analyst for the Tunisian market (as of April 2025).
Analyze user answers and job details. Provide concise justifications and match scores (0.0-1.0).
Your response MUST be a single, valid JSON object with one key match_results (a list of objects, each with job_id (string), match_score (float), reason (string)). Ensure an entry for every job ID provided."""
        llm_reasoning_prompt = "Analyze the following job matches based on the user's survey answers:\n\n"
        llm_reasoning_prompt += f"User Survey Answers:\njson\n{json.dumps(survey_answers, indent=2)}\n\n\n"
        llm_reasoning_prompt += "Job Details to Analyze:\n"
        for job in top_matches:
            job_detail = {k: v for k, v in job.items() if k not in ['calculated_score', 'source_url']}
            llm_reasoning_prompt += f"Job ID: {job.get('id')}\njson\n{json.dumps(job_detail, indent=2)}\n\n"

        messages = [{"role": "system", "content": system_prompt_match}, {"role": "user", "content": llm_reasoning_prompt}]
        log.info(f"Requesting LLM analysis for {len(top_matches)} potential job matches...")
        response_data = ask_llm(messages, model=MODEL_ANALYZE, temperature=0.15, json_mode=True)

        llm_matches_map = {}
        if response_data['success'] and isinstance(response_data['content'], dict) and 'match_results' in response_data['content'] and isinstance(response_data['content']['match_results'], list):
            log.info("LLM provided match analysis successfully.")
            for match_info in response_data['content']['match_results']:
                if isinstance(match_info, dict) and all(k in match_info for k in ['job_id', 'match_score', 'reason']):
                    try: 
                        score = min(max(float(match_info['match_score']), 0.0), 1.0)
                    except: 
                        score = 0.5
                    llm_matches_map[match_info['job_id']] = {'match_score': score, 'reason': str(match_info['reason'])}
                else: 
                    log.warning(f"LLM returned invalid item structure in 'match_results': {match_info}")
        else: 
            log.warning(f"LLM failed to provide valid match analysis JSON. Error: {response_data.get('error', 'Invalid structure')}")

        final_recommendations = []
        for job in top_matches:
            job_id = job.get('id')
            if job_id in llm_matches_map:
                job['match_score'] = llm_matches_map[job_id]['match_score']
                job['reason'] = llm_matches_map[job_id]['reason']
            else:
                job['match_score'] = job.get('calculated_score', 0.0)
                job['reason'] = "Basic score applied; LLM analysis unavailable/failed for this item."
            job.pop('calculated_score', None)
            final_recommendations.append(job)

        final_recommendations.sort(key=lambda x: x.get('match_score', 0.0), reverse=True)
        top_n_results = 5
        log.info(f"Returning top {min(len(final_recommendations), top_n_results)} recommendations.")
        return {'success': True, 'recommendations': final_recommendations[:top_n_results], 'error': None}
    else:
        log.info("No potential matches found after initial filtering.")
        return {'success': True, 'recommendations': [], 'error': "No suitable jobs found after filtering."}