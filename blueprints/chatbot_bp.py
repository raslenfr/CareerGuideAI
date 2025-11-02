"""
POST /api/chatbot/message
    ➤ Handles user messages for career advice via LLM.

Request Body:
{
    "message": "What career should I pursue after B.Tech CSE?",
    "history": [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ],
    "user_id": 1,
    "conversation_id": "uuid-string"
}

Response:
{
    "success": true,
    "reply": "Based on your CSE background, consider software development...",
    "history_update": [...],
    "conversation_id": "uuid-string"
}

GET /api/chatbot/conversations
    ➤ Get list of all user conversations (titles and metadata)

GET /api/chatbot/conversations/<conversation_id>
    ➤ Get full history of a specific conversation

DELETE /api/chatbot/conversations/<conversation_id>
    ➤ Delete a conversation
"""

from flask import Blueprint, request, jsonify
from services.llm_service import get_career_advice
from extensions import db
from models import ChatHistory
import logging
import uuid

# Get logger instance (child logger of the root logger configured in llm_service or app.py)
log = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot_bp', __name__, url_prefix='/api/chatbot')

def generate_chat_title(message):
    """Generate a title from the first message (truncate to ~50 chars)."""
    title = message[:50].strip()
    if len(message) > 50:
        title += "..."
    return title


@chatbot_bp.route('/message', methods=['POST'])
def handle_message():
    """Handles incoming chat messages for career guidance."""
    data = request.get_json()
    if not data or not isinstance(data, dict):
         log.warning("Chatbot request body is missing or not JSON")
         return jsonify({"success": False, "reply": None, "error": "Invalid request body. JSON object expected."}), 400

    user_message = data.get('message')
    history = data.get('history', [])
    user_id = data.get('user_id')  # Optional: user ID for saving
    conversation_id = data.get('conversation_id')  # Optional: existing conversation
    auto_save = data.get('auto_save', False)  # Explicit flag to enable auto-saving

    if not user_message or not isinstance(user_message, str) or len(user_message) > 2000:
        log.warning(f"Chatbot validation failed: Missing, invalid, or too long 'message'. Length: {len(user_message) if user_message else 'N/A'}")
        return jsonify({"success": False, "reply": None, "error": "Missing, invalid, or too long 'message' (string, max 2000 chars) in request body"}), 400
    if not isinstance(history, list):
        log.warning(f"Chatbot validation failed: Invalid 'history' format. Received type: {type(history)}")
        return jsonify({"success": False, "reply": None, "error": "Invalid 'history' format (must be a list)"}), 400

    log.info(f"Received chatbot message. History length: {len(history)}")
    response_data = get_career_advice(user_message, history)

    if response_data['success']:
        # Generate or use existing conversation ID
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            log.info(f"Created new conversation: {conversation_id}")
        
        # Save to database only if auto_save is enabled and user is authenticated
        if auto_save and user_id:
            try:
                # Check if this is first message in conversation
                existing_messages = ChatHistory.query.filter_by(conversation_id=conversation_id).count()
                chat_title = None
                
                if existing_messages == 0:
                    # First message - generate title
                    chat_title = generate_chat_title(user_message)
                    log.info(f"Generated chat title: {chat_title}")
                
                # Save the message exchange
                chat_record = ChatHistory(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    chat_title=chat_title,
                    message=user_message,
                    reply=response_data['reply']
                )
                db.session.add(chat_record)
                db.session.commit()
                log.info(f"Auto-saved chat message to database for user {user_id}")
                
            except Exception as e:
                db.session.rollback()
                log.error(f"Error auto-saving chat message: {e}")
                # Don't fail the request if saving fails
        
        current_interaction = []
        if user_message: current_interaction.append({"role": "user", "content": user_message})
        if response_data['reply']: current_interaction.append({"role": "assistant", "content": response_data['reply']})
        new_history = history + current_interaction
        history_limit = 10
        limited_history_update = new_history[-history_limit:]
        log.info(f"Chatbot reply generated successfully.")
        return jsonify({
            "success": True,
            "reply": response_data['reply'],
            "history_update": limited_history_update,
            "conversation_id": conversation_id
        })
    else:
        log.error(f"Chatbot error during LLM interaction: {response_data['error']}")
        status_code = 500
        if "client not initialized" in response_data.get('error', ''): status_code = 503
        elif "Rate Limit Error" in response_data.get('error', ''): status_code = 429
        return jsonify({"success": False, "reply": None, "error": response_data['error']}), status_code


@chatbot_bp.route('/save-conversation', methods=['POST'])
def save_conversation():
    """Save or update an entire conversation to the database."""
    data = request.get_json()
    
    if not data or not isinstance(data, dict):
        log.warning("Save conversation request body is missing or not JSON")
        return jsonify({"success": False, "error": "Invalid request body"}), 400
    
    user_id = data.get('user_id')
    messages = data.get('messages', [])
    conversation_id = data.get('conversation_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id is required"}), 400
    
    if not messages or len(messages) < 2:
        return jsonify({"success": False, "error": "At least one message exchange required"}), 400
    
    try:
        # Generate or use existing conversation ID
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            log.info(f"Created new conversation for saving: {conversation_id}")
        
        # Check if conversation already exists
        existing_messages = ChatHistory.query.filter_by(
            user_id=user_id,
            conversation_id=conversation_id
        ).order_by(ChatHistory.created_at.asc()).all()
        
        is_update = len(existing_messages) > 0
        
        # Get the count of existing message pairs (not individual messages)
        existing_pairs_count = len(existing_messages)
        
        # Generate title from first user message (only for new conversations)
        first_user_msg = None
        for msg in messages:
            if msg.get('role') == 'user':
                first_user_msg = msg.get('content')
                break
        
        chat_title = generate_chat_title(first_user_msg) if first_user_msg else "Untitled Chat"
        
        # Determine which messages are new (skip already saved ones)
        # Each existing record in DB represents one user+assistant pair
        # So if we have 3 records in DB, we've saved first 3 pairs (6 messages total)
        messages_to_skip = existing_pairs_count * 2  # 2 messages per pair
        new_messages = messages[messages_to_skip:]
        
        if not new_messages or len(new_messages) < 2:
            # No new messages to save
            if is_update:
                log.info(f"No new messages to add for conversation {conversation_id}")
                return jsonify({
                    "success": True,
                    "message": "Conversation already up to date",
                    "conversation_id": conversation_id,
                    "title": existing_messages[0].chat_title if existing_messages else chat_title,
                    "appended_count": 0,  # No new messages added
                    "is_update": True
                }), 200
        
        # Save new message pairs to database
        saved_count = 0
        for i in range(0, len(new_messages) - 1, 2):
            if i + 1 < len(new_messages):
                user_msg = new_messages[i]
                assistant_msg = new_messages[i + 1]
                
                if user_msg.get('role') == 'user' and assistant_msg.get('role') == 'assistant':
                    chat_record = ChatHistory(
                        user_id=user_id,
                        conversation_id=conversation_id,
                        chat_title=chat_title if not is_update and saved_count == 0 else None,
                        message=user_msg.get('content', ''),
                        reply=assistant_msg.get('content', '')
                    )
                    db.session.add(chat_record)
                    saved_count += 1
        
        db.session.commit()
        
        action = "Updated" if is_update else "Saved"
        log.info(f"{action} conversation {conversation_id} with {saved_count} new message pairs for user {user_id}")
        
        # Get the title from existing messages if updating
        final_title = existing_messages[0].chat_title if (is_update and existing_messages) else chat_title
        
        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "title": final_title,
            "message_count": saved_count,
            "appended_count": saved_count,  # Number of new message pairs added
            "message": f"Conversation {action.lower()} successfully",
            "is_update": is_update
        }), 200 if is_update else 201
        
    except Exception as e:
        db.session.rollback()
        log.error(f"Error saving conversation: {e}")
        return jsonify({"success": False, "error": "Failed to save conversation"}), 500


@chatbot_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Get list of all conversations for a user with title and metadata."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id parameter is required"}), 400
    
    try:
        # Get distinct conversations with their titles and first message date
        conversations = db.session.query(
            ChatHistory.conversation_id,
            db.func.min(ChatHistory.chat_title).label('title'),
            db.func.min(ChatHistory.created_at).label('created_at'),
            db.func.count(ChatHistory.id).label('message_count')
        ).filter_by(user_id=user_id).group_by(
            ChatHistory.conversation_id
        ).order_by(
            db.func.min(ChatHistory.created_at).desc()
        ).all()
        
        conversation_list = []
        for conv in conversations:
            # Get first message for preview
            first_message = ChatHistory.query.filter_by(
                user_id=user_id,
                conversation_id=conv.conversation_id
            ).order_by(ChatHistory.created_at.asc()).first()
            
            conversation_list.append({
                'conversation_id': conv.conversation_id,
                'title': conv.title or (first_message.message[:50] + "..." if first_message else "Untitled Chat"),
                'created_at': conv.created_at.isoformat() if conv.created_at else None,
                'message_count': conv.message_count,
                'preview': first_message.message[:100] if first_message else ""
            })
        
        log.info(f"Retrieved {len(conversation_list)} conversations for user {user_id}")
        return jsonify({"success": True, "conversations": conversation_list})
        
    except Exception as e:
        log.error(f"Error retrieving conversations: {e}")
        return jsonify({"success": False, "error": "Failed to retrieve conversations"}), 500


@chatbot_bp.route('/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get full history of a specific conversation."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id parameter is required"}), 400
    
    try:
        # Get all messages in this conversation
        messages = ChatHistory.query.filter_by(
            user_id=user_id,
            conversation_id=conversation_id
        ).order_by(ChatHistory.created_at.asc()).all()
        
        if not messages:
            return jsonify({"success": False, "error": "Conversation not found"}), 404
        
        # Format messages for frontend
        history = []
        for msg in messages:
            history.append({"role": "user", "content": msg.message})
            history.append({"role": "assistant", "content": msg.reply})
        
        conversation_data = {
            'conversation_id': conversation_id,
            'title': messages[0].chat_title or messages[0].message[:50],
            'created_at': messages[0].created_at.isoformat(),
            'history': history,
            'message_count': len(messages)
        }
        
        log.info(f"Retrieved conversation {conversation_id} with {len(messages)} message pairs")
        return jsonify({"success": True, "conversation": conversation_data})
        
    except Exception as e:
        log.error(f"Error retrieving conversation {conversation_id}: {e}")
        return jsonify({"success": False, "error": "Failed to retrieve conversation"}), 500


@chatbot_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all its messages."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "error": "user_id parameter is required"}), 400
    
    try:
        # Delete all messages in this conversation
        deleted_count = ChatHistory.query.filter_by(
            user_id=user_id,
            conversation_id=conversation_id
        ).delete()
        
        db.session.commit()
        
        if deleted_count == 0:
            return jsonify({"success": False, "error": "Conversation not found"}), 404
        
        log.info(f"Deleted conversation {conversation_id} ({deleted_count} messages) for user {user_id}")
        return jsonify({"success": True, "message": f"Deleted {deleted_count} messages"})
        
    except Exception as e:
        db.session.rollback()
        log.error(f"Error deleting conversation {conversation_id}: {e}")
        return jsonify({"success": False, "error": "Failed to delete conversation"}), 500
