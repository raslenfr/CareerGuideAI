"""
Enhanced Authentication with JWT (Integrated from Wissal Backend)
=================================================================

POST /api/auth/signup
    ➤ Register a new user account with JWT token

Request Body:
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "username": "johndoe" (optional)
}

Response:
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "username": "johndoe",
        "role": "student",
        "is_verified": false
    },
    "message": "Account created successfully"
}

POST /api/auth/login
    ➤ Authenticate user and return JWT token

Request Body:
{
    "email": "john@example.com",
    "password": "securepassword123"
}

Response:
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    },
    "message": "Login successful"
}

GET /api/auth/me
    ➤ Get current user information (requires JWT)

Headers:
    Authorization: Bearer <token>

Response:
{
    "success": true,
    "user": {...}
}
"""

from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User
from utils.jwt_helper import create_access_token
from utils.auth_decorators import require_auth
from utils.email_verification import generate_code, send_verification_code
from utils.email_welcome import send_welcome_email
from services.fraud_service import score_signup
from datetime import datetime, timedelta
import logging

log = logging.getLogger(__name__)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user account with JWT token generation."""
    data = request.get_json()
    
    # Validation
    if not data or not isinstance(data, dict):
        log.warning("Signup request body is missing or not JSON")
        return jsonify({"success": False, "error": "Invalid request body. JSON object expected."}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    username = data.get('username', email.split('@')[0]).strip()  # Default username from email
    role = data.get('role', 'student')  # Default role is student
    
    # Only allow 'student' or 'admin' roles (no teacher)
    if role not in ['student', 'admin']:
        role = 'student'
    
    # Validate required fields
    if not name or len(name) < 2:
        return jsonify({"success": False, "error": "Name is required (minimum 2 characters)"}), 400
    
    if not email or '@' not in email or len(email) < 5:
        return jsonify({"success": False, "error": "Valid email address is required"}), 400
    
    if not password or len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long"}), 400
    
    # Check if user already exists with same email AND role
    existing_user_same_role = User.query.filter(
        (User.email == email) & (User.role == role)
    ).first()
    
    if existing_user_same_role:
        log.warning(f"Signup attempt with existing email+role: {email} as {role}")
        return jsonify({"success": False, "error": f"A {role} account with this email already exists"}), 400
    
    # Check if username is already taken (username must be globally unique)
    if username:
        existing_username = User.query.filter(User.username == username).first()
        if existing_username:
            log.warning(f"Signup attempt with existing username: {username}")
            return jsonify({"success": False, "error": "This username is already taken"}), 400
    
    try:
        # Hash the password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user with enhanced fields
        new_user = User(
            name=name,
            email=email,
            username=username,
            full_name=name,
            password_hash=password_hash,
            role=role,
            is_verified=False  # New users need to verify email
        )
        
        # ML-powered fraud detection
        try:
            risk_score, is_suspicious, fraud_reason = score_signup(
                username=username,
                email=email,
                full_name=name,
                request_context={'ip': request.remote_addr}
            )
            new_user.risk_score = risk_score
            new_user.is_suspicious = is_suspicious
            new_user.fraud_reason = fraud_reason
            new_user.fraud_checked_at = datetime.utcnow()
            
            if is_suspicious:
                log.warning(f"Suspicious signup detected: {email} (score: {risk_score}, reason: {fraud_reason})")
            else:
                log.info(f"Fraud check passed: {email} (score: {risk_score})")
        except Exception as fraud_err:
            # Don't block signup if fraud detection fails
            log.error(f"Fraud detection error for {email}: {fraud_err}")
            new_user.risk_score = None
            new_user.is_suspicious = False
            new_user.fraud_reason = "error: fraud check failed"
        
        # TEMPORARY: Auto-verify users for testing (no email verification flow)
        new_user.is_verified = True
        new_user.verification_code = None
        new_user.verification_sent_at = None
        
        db.session.add(new_user)
        db.session.commit()
        
        log.info(f"New user registered: {email} (username: {username}, fraud_score: {new_user.risk_score})")
        
        # For testing: return success and optional token, but frontend will redirect to login
        access_token = create_access_token({
            "sub": new_user.username,
            "user_id": new_user.id,
            "role": new_user.role
        })
        return jsonify({
            "success": True,
            "message": "Account created successfully.",
            "email_sent": False,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": new_user.email,
                "name": new_user.name,
                "role": new_user.role,
                "is_verified": new_user.is_verified
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        log.exception(f"Error during signup: {e}")
        return jsonify({"success": False, "error": "An error occurred during registration. Please try again."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    
    # Validation
    if not data or not isinstance(data, dict):
        log.warning("Login request body is missing or not JSON")
        return jsonify({"success": False, "error": "Invalid request body. JSON object expected."}), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', '').strip().lower()  # Optional: specify which account to login to
    
    # Validate required fields
    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required"}), 400
    
    try:
        # Find user by email OR username (support both)
        # If role is specified, filter by role as well
        if role and role in ['student', 'admin']:
            user = User.query.filter(
                ((User.email == email) | (User.username == email)) & (User.role == role)
            ).first()
        else:
            user = User.query.filter(
                (User.email == email) | (User.username == email)
            ).first()
        
        if not user:
            log.warning(f"Login attempt with non-existent email/username: {email}")
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
        
        # Verify password
        if not bcrypt.check_password_hash(user.password_hash, password):
            log.warning(f"Failed login attempt for user: {email}")
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
        
        # TEMPORARY: Do not block login by verification status (testing mode)
        
        log.info(f"User logged in successfully: {email} (ID: {user.id})")
        
        # Generate JWT token
        access_token = create_access_token({
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        })
        
        return jsonify({
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict(),
            "message": "Login successful"
        }), 200
        
    except Exception as e:
        log.exception(f"Error during login: {e}")
        return jsonify({"success": False, "error": "An error occurred during login. Please try again."}), 500


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information from JWT token."""
    try:
        user_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        log.exception(f"Error fetching current user: {e}")
        return jsonify({"success": False, "error": "Failed to fetch user information"}), 500


@auth_bp.route('/send-verification', methods=['POST'])
@require_auth
def send_verification():
    """Send email verification code to user."""
    try:
        user_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        if user.is_verified:
            return jsonify({"success": False, "error": "Email already verified"}), 400
        
        # Generate 6-digit code
        code = generate_code()
        user.verification_code = code
        user.verification_sent_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send email
        send_verification_code(user.email, code, user.name)
        
        log.info(f"Verification code sent to {user.email}")
        
        return jsonify({
            "success": True,
            "message": "Verification code sent to your email"
        }), 200
        
    except Exception as e:
        log.exception(f"Error sending verification code: {e}")
        return jsonify({"success": False, "error": "Failed to send verification code"}), 500


@auth_bp.route('/verify-email', methods=['POST'])
@require_auth
def verify_email():
    """Verify email with code."""
    data = request.get_json()
    code = data.get('code')
    
    if not code or len(code) != 6:
        return jsonify({"success": False, "error": "Invalid code format"}), 400
    
    try:
        user_id = request.user_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        if user.is_verified:
            return jsonify({"success": False, "error": "Already verified"}), 400
        
        # Check code match
        if user.verification_code != code:
            return jsonify({"success": False, "error": "Invalid verification code"}), 400
        
        # Check expiration (10 minutes)
        if user.verification_sent_at:
            expiry_time = user.verification_sent_at + timedelta(minutes=10)
            if datetime.utcnow() > expiry_time:
                return jsonify({"success": False, "error": "Verification code expired"}), 400
        
        # Verify user
        user.is_verified = True
        user.verification_code = None
        user.verification_sent_at = None
        
        db.session.commit()
        
        # Send welcome email
        try:
            send_welcome_email(user.email, user.name)
        except Exception as e:
            log.error(f"Failed to send welcome email: {e}")
        
        log.info(f"Email verified for {user.email}")
        
        return jsonify({
            "success": True,
            "message": "Email verified successfully! You can now login.",
            "user": user.to_dict(),
            "redirect_to_login": True
        }), 200
        
    except Exception as e:
        log.exception(f"Error verifying email: {e}")
        return jsonify({"success": False, "error": "Verification failed"}), 500

