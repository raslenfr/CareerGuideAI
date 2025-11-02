"""
Test Recording Blueprint
Handles real-time AI interaction logging for frontend-integrated testing
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import json
import logging
from typing import Dict, List, Any

log = logging.getLogger(__name__)

test_recording_bp = Blueprint('test_recording', __name__, url_prefix='/api/tests')

# In-memory storage for active test sessions
# Format: {session_id: {ai_type: [interactions], metadata: {...}}}
active_sessions: Dict[str, Dict[str, Any]] = {}


@test_recording_bp.route('/start-recording', methods=['POST'])
def start_recording():
    """
    Start a new test recording session
    Returns a session_id for tracking interactions
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session storage
        active_sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'started_at': datetime.utcnow().isoformat(),
            'interactions': {
                'chatbot': [],
                'career_suggester': [],
                'course_recommender': []
            },
            'metadata': {
                'total_interactions': 0,
                'ai_types_tested': set()
            }
        }
        
        log.info(f"Started test recording session: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Test recording started',
            'started_at': active_sessions[session_id]['started_at']
        }), 201
        
    except Exception as e:
        log.error(f"Error starting test recording: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@test_recording_bp.route('/log-interaction', methods=['POST'])
def log_interaction():
    """
    Log an AI interaction during test recording
    Automatically detects AI type based on current page/component
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        session_id = data.get('session_id')
        ai_type = data.get('ai_type')  # 'chatbot', 'career_suggester', 'course_recommender'
        interaction_data = data.get('interaction')
        
        # Validate required fields
        if not session_id or not ai_type or not interaction_data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: session_id, ai_type, interaction'
            }), 400
        
        # Check if session exists
        if session_id not in active_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session_id or session expired'
            }), 404
        
        # Validate AI type
        valid_ai_types = ['chatbot', 'career_suggester', 'course_recommender']
        if ai_type not in valid_ai_types:
            return jsonify({
                'success': False,
                'error': f'Invalid ai_type. Must be one of: {valid_ai_types}'
            }), 400
        
        # Add timestamp to interaction
        interaction_data['timestamp'] = datetime.utcnow().isoformat()
        interaction_data['interaction_id'] = str(uuid.uuid4())
        
        # Store interaction
        session = active_sessions[session_id]
        session['interactions'][ai_type].append(interaction_data)
        session['metadata']['total_interactions'] += 1
        session['metadata']['ai_types_tested'].add(ai_type)
        
        log.info(f"Logged {ai_type} interaction for session {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Interaction logged',
            'interaction_id': interaction_data['interaction_id'],
            'total_interactions': session['metadata']['total_interactions']
        }), 200
        
    except Exception as e:
        log.error(f"Error logging interaction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@test_recording_bp.route('/stop-recording', methods=['POST'])
def stop_recording():
    """
    Stop test recording and generate comprehensive diagnostic report
    """
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'session_id required'}), 400
        
        if session_id not in active_sessions:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Get session data
        session = active_sessions[session_id]
        stopped_at = datetime.utcnow().isoformat()
        
        # Calculate session duration
        started_at = datetime.fromisoformat(session['started_at'])
        ended_at = datetime.utcnow()
        duration_seconds = (ended_at - started_at).total_seconds()
        
        # Generate report for each AI type
        reports = {}
        overall_score = 0
        total_ai_types = 0
        
        for ai_type, interactions in session['interactions'].items():
            if interactions:  # Only analyze if there are interactions
                report = _analyze_interactions(ai_type, interactions, duration_seconds)
                reports[ai_type] = report
                overall_score += report['score']
                total_ai_types += 1
        
        # Calculate average score
        avg_score = overall_score / total_ai_types if total_ai_types > 0 else 0
        
        # Build comprehensive report
        comprehensive_report = {
            'test_id': f"frontend_recording_{session_id[:8]}",
            'session_id': session_id,
            'timestamp': stopped_at,
            'test_name': 'Frontend AI Test Recording',
            'test_type': 'frontend_integrated',
            'status': 'PASS' if avg_score >= 70 else 'WARNING' if avg_score >= 50 else 'FAIL',
            'overall_score': round(avg_score, 2),
            'duration_seconds': round(duration_seconds, 2),
            'summary': {
                'started_at': session['started_at'],
                'stopped_at': stopped_at,
                'total_interactions': session['metadata']['total_interactions'],
                'ai_types_tested': list(session['metadata']['ai_types_tested']),
                'user_id': session.get('user_id')
            },
            'ai_reports': reports,
            'metadata': {
                'test_mode': 'frontend_recording',
                'manual_control': True
            }
        }
        
        # Save report to file
        try:
            import os
            logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            
            timestamp_str = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"ai_diagnostic_frontend_recording_{timestamp_str}.json"
            filepath = os.path.join(logs_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report, f, indent=2, ensure_ascii=False)
            
            comprehensive_report['report_file'] = filename
            log.info(f"Saved test report to: {filepath}")
            
        except Exception as e:
            log.error(f"Error saving report file: {e}")
            comprehensive_report['report_file'] = None
        
        # Clean up session
        del active_sessions[session_id]
        
        log.info(f"Stopped test recording session {session_id}, generated report")
        
        return jsonify({
            'success': True,
            'message': 'Test recording stopped',
            'report': comprehensive_report
        }), 200
        
    except Exception as e:
        log.error(f"Error stopping test recording: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@test_recording_bp.route('/session-status/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get current status of an active test recording session"""
    try:
        if session_id not in active_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session = active_sessions[session_id]
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'started_at': session['started_at'],
            'total_interactions': session['metadata']['total_interactions'],
            'ai_types_tested': list(session['metadata']['ai_types_tested']),
            'interactions_by_type': {
                ai_type: len(interactions)
                for ai_type, interactions in session['interactions'].items()
            }
        }), 200
        
    except Exception as e:
        log.error(f"Error getting session status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _analyze_interactions(ai_type: str, interactions: List[Dict], duration: float) -> Dict[str, Any]:
    """Analyze interactions and generate quality report"""
    
    total_interactions = len(interactions)
    quality_scores = []
    issues = []
    
    for idx, interaction in enumerate(interactions):
        # Analyze each interaction based on AI type
        if ai_type == 'chatbot':
            score = _analyze_chatbot_interaction(interaction, idx)
        elif ai_type == 'career_suggester':
            score = _analyze_suggester_interaction(interaction, idx)
        elif ai_type == 'course_recommender':
            score = _analyze_recommender_interaction(interaction, idx)
        else:
            score = 50  # Default score
        
        quality_scores.append(score)
        
        # Log issues for low-quality interactions
        if score < 70:
            issues.append({
                'severity': 'WARNING' if score >= 50 else 'ERROR',
                'description': f'{ai_type} interaction {idx + 1}: Low quality score',
                'details': f'Score: {score}/100',
                'timestamp': interaction.get('timestamp')
            })
    
    # Calculate metrics
    avg_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
    avg_response_time = sum(
        interaction.get('response_time_ms', 0) for interaction in interactions
    ) / total_interactions if total_interactions > 0 else 0
    
    return {
        'ai_type': ai_type,
        'score': round(avg_score, 2),
        'total_interactions': total_interactions,
        'avg_response_time_ms': round(avg_response_time, 2),
        'quality_scores': quality_scores,
        'issues': issues,
        'status': 'PASS' if avg_score >= 70 else 'WARNING' if avg_score >= 50 else 'FAIL'
    }


def _analyze_chatbot_interaction(interaction: Dict, idx: int) -> int:
    """Analyze chatbot interaction quality"""
    score = 100
    
    user_message = interaction.get('user_message', '')
    ai_response = interaction.get('ai_response', '')
    
    # Check response length
    if len(ai_response) < 20:
        score -= 30
    elif len(ai_response) > 3000:
        score -= 10
    
    # Check for career-related keywords
    career_keywords = [
        'career', 'job', 'skill', 'education', 'certification',
        'industry', 'profession', 'role', 'experience', 'training'
    ]
    career_keyword_count = sum(1 for keyword in career_keywords if keyword.lower() in ai_response.lower())
    
    if career_keyword_count == 0:
        score -= 40
    elif career_keyword_count < 2:
        score -= 20
    
    # Check relevance
    if user_message and ai_response:
        user_words = set(user_message.lower().split())
        response_words = set(ai_response.lower().split())
        overlap = len(user_words & response_words)
        
        if overlap < 2:
            score -= 20
    
    return max(0, score)


def _analyze_suggester_interaction(interaction: Dict, idx: int) -> int:
    """Analyze career suggester interaction quality"""
    score = 100
    
    suggestions = interaction.get('suggestions', [])
    answer = interaction.get('answer', '')
    is_final = interaction.get('is_final', False)
    
    # Only check suggestions for final interaction
    if is_final:
        if not suggestions:
            score -= 50
        elif len(suggestions) < 3:
            score -= 20
    
    # Check answer quality (for both intermediate and final)
    if not answer or len(answer) < 5:
        score -= 30
    
    return max(0, score)


def _analyze_recommender_interaction(interaction: Dict, idx: int) -> int:
    """Analyze course recommender interaction quality"""
    score = 100
    
    courses = interaction.get('courses', [])
    keywords = interaction.get('keywords', '')
    
    # Check if courses exist
    if not courses:
        score -= 50
    elif len(courses) < 3:
        score -= 20
    
    # Check keyword relevance
    if not keywords or len(keywords) < 3:
        score -= 30
    
    return max(0, score)


log.info("Test Recording Blueprint loaded")

