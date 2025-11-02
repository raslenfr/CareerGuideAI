"""
Authentication and Authorization Decorators (from Wissal Backend)
================================================================
This module provides decorators for protecting routes with JWT authentication
and role-based access control.
"""

from functools import wraps
from flask import request, jsonify
from utils.jwt_helper import get_token_from_header, decode_token
import logging

log = logging.getLogger(__name__)


def require_auth(func):
    """
    Decorator to require valid JWT token for accessing a route.
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user_id = request.user_data.get('user_id')
            return {"message": "Access granted"}
    
    The decoded token payload is attached to request.user_data
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = get_token_from_header(auth_header)
        
        if not token:
            log.warning(f"Missing auth token for {request.path}")
            return jsonify({"success": False, "error": "Authentication required"}), 401
        
        payload = decode_token(token)
        
        if not payload:
            log.warning(f"Invalid token for {request.path}")
            return jsonify({"success": False, "error": "Invalid or expired token"}), 401
        
        # Attach user info to request context
        request.user_data = payload
        
        return func(*args, **kwargs)
    
    return wrapper


def require_role(role: str):
    """
    Decorator to require a specific role for accessing a route.
    
    Args:
        role: Required role ('admin', 'teacher', or 'student')
    
    Usage:
        @app.route('/admin')
        @require_role('admin')
        def admin_route():
            return {"message": "Admin access granted"}
    
    Note: This decorator automatically includes @require_auth
    """
    def decorator(func):
        @wraps(func)
        @require_auth
        def wrapper(*args, **kwargs):
            user_role = request.user_data.get('role')
            
            if user_role != role:
                log.warning(f"Insufficient permissions: {user_role} != {role} for {request.path}")
                return jsonify({
                    "success": False, 
                    "error": f"Access denied. Required role: {role}"
                }), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_admin(func):
    """
    Decorator to require admin role.
    
    Usage:
        @app.route('/admin/users')
        @require_admin
        def list_users():
            return {"users": [...]}
    
    This is a convenience wrapper for @require_role('admin')
    """
    return require_role('admin')(func)


def require_teacher_or_admin(func):
    """
    Decorator to require either teacher or admin role.
    
    Usage:
        @app.route('/courses/create')
        @require_teacher_or_admin
        def create_course():
            return {"message": "Course created"}
    """
    @wraps(func)
    @require_auth
    def wrapper(*args, **kwargs):
        user_role = request.user_data.get('role')
        
        if user_role not in ['admin', 'teacher']:
            log.warning(f"Insufficient permissions: {user_role} for {request.path}")
            return jsonify({
                "success": False, 
                "error": "Access denied. Teacher or Admin role required"
            }), 403
        
        return func(*args, **kwargs)
    
    return wrapper


def optional_auth(func):
    """
    Decorator that adds user_data if token is provided, but doesn't require it.
    
    Usage:
        @app.route('/public-but-personalized')
        @optional_auth
        def route():
            if hasattr(request, 'user_data'):
                return {"message": f"Hello {request.user_data['sub']}"}
            return {"message": "Hello guest"}
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = get_token_from_header(auth_header)
        
        if token:
            payload = decode_token(token)
            if payload:
                request.user_data = payload
        
        return func(*args, **kwargs)
    
    return wrapper

