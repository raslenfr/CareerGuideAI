"""
JWT Token Creation and Validation Utilities (from Wissal Backend)
================================================================
This module provides JWT token management for authentication.
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
import logging

log = logging.getLogger(__name__)

# JWT Configuration (read from environment variables)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-default-secret-key-CHANGE-IN-PRODUCTION")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))

if SECRET_KEY == "your-default-secret-key-CHANGE-IN-PRODUCTION":
    log.warning("⚠️ Using default JWT_SECRET_KEY! Set JWT_SECRET_KEY in .env for production!")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with user data.
    
    Args:
        data: Dictionary with user info (typically {'sub': username, 'user_id': id, 'role': role})
        expires_delta: Optional custom expiration time
    
    Returns:
        JWT token string
    
    Example:
        token = create_access_token({'sub': 'john_doe', 'user_id': 1, 'role': 'student'})
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    log.info(f"Created JWT token for user: {data.get('sub')}")
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dict or None if invalid
    
    Example:
        payload = decode_token(token)
        if payload:
            user_id = payload.get('user_id')
            role = payload.get('role')
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            log.warning("Token has no 'sub' claim")
            return None
        
        return payload
        
    except JWTError as e:
        log.warning(f"JWT validation failed: {e}")
        return None


def get_token_from_header(authorization: str) -> Optional[str]:
    """
    Extract JWT token from Authorization header.
    
    Args:
        authorization: Header value (e.g., "Bearer <token>")
    
    Returns:
        Token string or None if invalid format
    
    Example:
        auth_header = request.headers.get('Authorization')
        token = get_token_from_header(auth_header)
    """
    if not authorization:
        return None
    
    parts = authorization.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]


def verify_token_expiry(token: str) -> bool:
    """
    Check if a token is expired without raising an exception.
    
    Args:
        token: JWT token string
    
    Returns:
        True if token is valid and not expired, False otherwise
    """
    payload = decode_token(token)
    if not payload:
        return False
    
    exp = payload.get('exp')
    if not exp:
        return False
    
    # Check if token is expired
    expiry_time = datetime.fromtimestamp(exp)
    return datetime.utcnow() < expiry_time

