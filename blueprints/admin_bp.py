"""
Admin Panel Blueprint (from Wissal Backend - Enhanced)
=====================================================
Provides user management and administrative functions.

All endpoints require admin role.
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models import User, AdminLog
from utils.auth_decorators import require_admin, require_auth
import logging

log = logging.getLogger(__name__)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/admin')


def log_admin_action(admin_id: int, action: str, target_user_id: int = None, details: str = None):
    """Helper function to log admin actions for audit trail."""
    try:
        log_entry = AdminLog(
            admin_id=admin_id,
            action=action,
            target_user_id=target_user_id,
            details=details
        )
        db.session.add(log_entry)
        db.session.commit()
        log.info(f"Admin action logged: {action} by admin {admin_id}")
    except Exception as e:
        log.error(f"Failed to log admin action: {e}")


@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    """
    List all users (admin only).
    
    Returns:
        List of all users with their details
    """
    try:
        users = User.query.all()
        
        log.info(f"Admin {request.user_data.get('user_id')} retrieved all users list")
        
        return jsonify({
            "success": True,
            "users": [user.to_dict() for user in users],
            "total": len(users)
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching users: {e}")
        return jsonify({"success": False, "error": "Failed to fetch users"}), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """
    Get specific user details (admin only).
    
    Args:
        user_id: ID of user to retrieve
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching user {user_id}: {e}")
        return jsonify({"success": False, "error": "Failed to fetch user"}), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id):
    """
    Update user details (admin only).
    
    Args:
        user_id: ID of user to update
    
    Request Body:
        {
            "email": "new@example.com",
            "name": "New Name",
            "role": "teacher",
            "permissions": ["view_courses", "edit_content"]
        }
    """
    data = request.get_json()
    
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Invalid request body"}), 400
    
    try:
        admin_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        # Prevent modifying other admins
        if user.role == 'admin' and user.id != admin_id:
            return jsonify({"success": False, "error": "Cannot modify other admin accounts"}), 403
        
        changes = []
        
        # Update allowed fields
        if 'email' in data and data['email'] != user.email:
            # Check email uniqueness
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({"success": False, "error": "Email already in use"}), 400
            user.email = data['email']
            changes.append(f"email -> {data['email']}")
        
        if 'name' in data:
            user.name = data['name']
            user.full_name = data['name']
            changes.append(f"name -> {data['name']}")
        
        if 'role' in data and data['role'] in ['admin', 'student']:
            old_role = user.role
            user.role = data['role']
            changes.append(f"role: {old_role} -> {data['role']}")
        
        if 'permissions' in data and isinstance(data['permissions'], list):
            user.permissions = ','.join(data['permissions'])
            changes.append(f"permissions updated")
        
        if 'is_verified' in data and isinstance(data['is_verified'], bool):
            user.is_verified = data['is_verified']
            changes.append(f"is_verified -> {data['is_verified']}")
        
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id,
            "update_user",
            user_id,
            f"Updated user {user.email}: {', '.join(changes)}"
        )
        
        log.info(f"Admin {admin_id} updated user {user_id}: {', '.join(changes)}")
        
        return jsonify({
            "success": True,
            "message": "User updated successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.exception(f"Error updating user {user_id}: {e}")
        return jsonify({"success": False, "error": "Failed to update user"}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """
    Delete a user (admin only).
    
    Args:
        user_id: ID of user to delete
    """
    try:
        admin_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        # Prevent deleting other admins
        if user.role == 'admin' and user.id != admin_id:
            return jsonify({"success": False, "error": "Cannot delete other admin accounts"}), 403
        
        # Prevent self-deletion
        if user.id == admin_id:
            return jsonify({"success": False, "error": "Cannot delete your own account"}), 403
        
        email = user.email
        db.session.delete(user)
        db.session.commit()
        
        # Log admin action
        log_admin_action(admin_id, "delete_user", user_id, f"Deleted user: {email}")
        
        log.info(f"Admin {admin_id} deleted user {user_id} ({email})")
        
        return jsonify({
            "success": True,
            "message": f"User {email} deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.exception(f"Error deleting user {user_id}: {e}")
        return jsonify({"success": False, "error": "Failed to delete user"}), 500


@admin_bp.route('/users/<int:user_id>/verify', methods=['PUT'])
@require_admin
def verify_user(user_id):
    """
    Manually verify a user's email (admin only).
    
    Args:
        user_id: ID of user to verify
    """
    try:
        admin_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        if user.is_verified:
            return jsonify({"success": False, "error": "User already verified"}), 400
        
        user.is_verified = True
        user.verification_code = None
        user.verification_sent_at = None
        
        db.session.commit()
        
        # Log admin action
        log_admin_action(admin_id, "verify_user", user_id, f"Manually verified user: {user.email}")
        
        log.info(f"Admin {admin_id} manually verified user {user_id}")
        
        return jsonify({
            "success": True,
            "message": "User verified successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.exception(f"Error verifying user {user_id}: {e}")
        return jsonify({"success": False, "error": "Failed to verify user"}), 500


@admin_bp.route('/stats', methods=['GET'])
@require_admin
def get_stats():
    """
    Get user statistics (admin only).
    
    Returns:
        Statistics about users (total, verified, roles, etc.)
    """
    try:
        total = User.query.count()
        verified = User.query.filter_by(is_verified=True).count()
        unverified = total - verified
        
        by_role = {
            "admin": User.query.filter_by(role='admin').count(),
            "student": User.query.filter_by(role='student').count()
        }
        
        log.info(f"Admin {request.user_data.get('user_id')} retrieved stats")
        
        return jsonify({
            "success": True,
            "stats": {
                "total": total,
                "verified": verified,
                "unverified": unverified,
                "verification_rate": round((verified / total) * 100, 2) if total > 0 else 0,
                "roles": by_role
            }
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching stats: {e}")
        return jsonify({"success": False, "error": "Failed to fetch statistics"}), 500


@admin_bp.route('/logs', methods=['GET'])
@require_admin
def get_logs():
    """
    Get admin action logs (admin only).
    
    Query Parameters:
        limit: Number of logs to retrieve (default 100)
    
    Returns:
        List of admin actions
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        limit = min(limit, 1000)  # Max 1000 logs
        
        logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(limit).all()
        
        log.info(f"Admin {request.user_data.get('user_id')} retrieved {len(logs)} logs")
        
        return jsonify({
            "success": True,
            "logs": [log_entry.to_dict() for log_entry in logs],
            "count": len(logs)
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching logs: {e}")
        return jsonify({"success": False, "error": "Failed to fetch logs"}), 500


@admin_bp.route('/users/search', methods=['GET'])
@require_admin
def search_users():
    """
    Search users by email, username, or name (admin only).
    
    Query Parameters:
        q: Search query
    
    Returns:
        List of matching users
    """
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({"success": False, "error": "Search query must be at least 2 characters"}), 400
    
    try:
        users = User.query.filter(
            (User.email.ilike(f'%{query}%')) |
            (User.username.ilike(f'%{query}%')) |
            (User.name.ilike(f'%{query}%'))
        ).all()
        
        log.info(f"Admin {request.user_data.get('user_id')} searched for: {query}")
        
        return jsonify({
            "success": True,
            "users": [user.to_dict() for user in users],
            "count": len(users)
        }), 200
        
    except Exception as e:
        log.exception(f"Error searching users: {e}")
        return jsonify({"success": False, "error": "Search failed"}), 500


# ==============================================================================
# FRAUD DETECTION ENDPOINTS
# ==============================================================================

@admin_bp.route('/fraud/queue', methods=['GET'])
@require_admin
def get_fraud_queue():
    """
    Get list of suspicious signups flagged for review.
    
    Query Parameters:
        page: Page number (default 1)
        per_page: Items per page (default 50)
        status: Filter by status - 'pending', 'reviewed', 'all' (default 'pending')
    
    Returns:
        List of users flagged as suspicious with fraud details
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status', 'pending')
        
        # Build query
        query = User.query.filter(User.is_suspicious == True)
        
        if status == 'pending':
            # Not yet reviewed
            query = query.filter(User.fraud_reviewed_by == None)
        elif status == 'reviewed':
            # Already reviewed
            query = query.filter(User.fraud_reviewed_by != None)
        # 'all' returns everything
        
        # Order by risk score (highest first), then creation date
        query = query.order_by(User.risk_score.desc(), User.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        users = [user.to_dict(include_fraud=True) for user in paginated.items]
        
        log.info(f"Admin {request.user_data.get('user_id')} retrieved fraud queue (status: {status})")
        
        return jsonify({
            "success": True,
            "users": users,
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "pages": paginated.pages
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching fraud queue: {e}")
        return jsonify({"success": False, "error": "Failed to fetch fraud queue"}), 500


@admin_bp.route('/fraud/stats', methods=['GET'])
@require_admin
def get_fraud_stats():
    """
    Get fraud detection statistics.
    
    Returns:
        Statistics about suspicious signups and fraud detection performance
    """
    try:
        from services.fraud_service import get_fraud_stats
        from sqlalchemy import func
        
        # Model stats
        model_stats = get_fraud_stats()
        
        # User stats
        total_users = User.query.count()
        suspicious_count = User.query.filter(User.is_suspicious == True).count()
        reviewed_count = User.query.filter(
            (User.is_suspicious == True) & (User.fraud_reviewed_by != None)
        ).count()
        pending_review = suspicious_count - reviewed_count
        
        # Average risk score for suspicious users
        avg_risk = db.session.query(func.avg(User.risk_score)).filter(
            User.is_suspicious == True
        ).scalar() or 0.0
        
        # By role breakdown
        suspicious_by_role = db.session.query(
            User.role,
            func.count(User.id).label('count')
        ).filter(User.is_suspicious == True).group_by(User.role).all()
        
        role_breakdown = {role: count for role, count in suspicious_by_role}
        
        # By fraud reason
        fraud_reasons = db.session.query(
            User.fraud_reason,
            func.count(User.id).label('count')
        ).filter(User.is_suspicious == True).group_by(User.fraud_reason).all()
        
        reason_breakdown = {reason: count for reason, count in fraud_reasons if reason}
        
        log.info(f"Admin {request.user_data.get('user_id')} retrieved fraud stats")
        
        return jsonify({
            "success": True,
            "stats": {
                "total_users": total_users,
                "suspicious_count": suspicious_count,
                "reviewed_count": reviewed_count,
                "pending_review": pending_review,
                "avg_risk_score": round(avg_risk, 4),
                "suspicious_percentage": round((suspicious_count / total_users * 100), 2) if total_users > 0 else 0,
                "by_role": role_breakdown,
                "by_reason": reason_breakdown
            },
            "model": model_stats
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching fraud stats: {e}")
        return jsonify({"success": False, "error": "Failed to fetch fraud stats"}), 500


@admin_bp.route('/fraud/review/<int:user_id>', methods=['POST'])
@require_admin
def review_fraud_case(user_id):
    """
    Review a fraud case and take action.
    
    Args:
        user_id: ID of user to review
    
    Request Body:
        {
            "action": "verify" | "block" | "clear",
            "note": "Admin's review notes (optional)"
        }
    
    Actions:
        - verify: Mark as legitimate, clear suspicious flag
        - block: Block/disable the account
        - clear: Clear suspicious flag without other action
    """
    data = request.get_json()
    
    if not data or 'action' not in data:
        return jsonify({"success": False, "error": "Action is required"}), 400
    
    action = data.get('action')
    note = data.get('note', '')
    
    if action not in ['verify', 'block', 'clear']:
        return jsonify({"success": False, "error": "Invalid action. Use verify, block, or clear."}), 400
    
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        admin_id = request.user_data.get('user_id')
        
        if action == 'verify':
            # Mark as verified and clear suspicious flag
            user.is_suspicious = False
            user.fraud_reviewed_by = admin_id
            user.fraud_review_note = note or "Reviewed and verified by admin"
            user.fraud_reason = "admin-verified"
            action_desc = "verified as legitimate"
            
        elif action == 'block':
            # Block the account
            user.is_suspicious = True  # Keep flag
            user.fraud_reviewed_by = admin_id
            user.fraud_review_note = note or "Blocked by admin"
            user.fraud_reason = "admin-blocked"
            user.permissions = "blocked"  # Block permissions
            action_desc = "blocked"
            
        elif action == 'clear':
            # Just clear the suspicious flag
            user.is_suspicious = False
            user.fraud_reviewed_by = admin_id
            user.fraud_review_note = note or "Cleared by admin"
            user.fraud_reason = "admin-cleared"
            action_desc = "cleared"
        
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id=admin_id,
            action=f"fraud_review_{action}",
            target_user_id=user_id,
            details=f"Fraud case {action_desc}. Note: {note}"
        )
        
        log.info(f"Admin {admin_id} {action_desc} fraud case for user {user_id} (risk: {user.risk_score})")
        
        return jsonify({
            "success": True,
            "message": f"User {action_desc} successfully",
            "user": user.to_dict(include_fraud=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        log.exception(f"Error reviewing fraud case {user_id}: {e}")
        return jsonify({"success": False, "error": "Failed to review fraud case"}), 500

