"""
Fraud Detection Service - ML-powered signup risk scoring
=========================================================
Uses a trained Logistic Regression model to detect suspicious signup patterns.
"""

import os
import json
import math
import joblib
import pandas as pd
import logging
from collections import Counter
from typing import Dict, Tuple, Optional

log = logging.getLogger(__name__)

# Configuration from environment
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.environ.get("FRAUD_MODEL_PATH", os.path.join(BASE_DIR, "ml_models", "signup_risk_model.joblib"))
THRESHOLDS_PATH = os.environ.get("FRAUD_THRESHOLDS_PATH", os.path.join(BASE_DIR, "ml_models", "signup_risk_thresholds.json"))
FEATURE_NAMES_PATH = os.environ.get("FRAUD_FEATURE_NAMES_PATH", os.path.join(BASE_DIR, "ml_models", "feature_names.json"))

# Thresholds
T_REVIEW = float(os.environ.get("FRAUD_THRESHOLD_REVIEW", 0.4))
T_BLOCK = float(os.environ.get("FRAUD_THRESHOLD_BLOCK", 0.8))

# Blacklists and known domains
DISPOSABLE_DOMAINS = {
    "yopmail.com", "mailinator.com", "tempmail.com", "10minutemail.com",
    "guerrillamail.com", "throwaway.email", "maildrop.cc", "getnada.com"
}

BLACKLIST = {"killer", "admin", "root", "test", "hack", "xxx", "spam", "bot", "fake"}

KNOWN_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
    "live.com", "msn.com", "aol.com", "protonmail.com"
}

# Global model instance
_model = None
_thresholds = {"T_REVIEW": T_REVIEW, "T_BLOCK": T_BLOCK}
_feature_names = []


def load_model():
    """Load the ML model, thresholds, and feature names at startup."""
    global _model, _thresholds, _feature_names
    
    try:
        if not os.path.exists(MODEL_PATH):
            log.warning(f"Fraud model not found at {MODEL_PATH}. Fraud detection disabled.")
            return False
        
        _model = joblib.load(MODEL_PATH)
        log.info(f"Fraud detection model loaded from {MODEL_PATH}")
        
        # Load thresholds if available
        if os.path.exists(THRESHOLDS_PATH):
            with open(THRESHOLDS_PATH, "r") as f:
                loaded_thresholds = json.load(f)
                _thresholds.update(loaded_thresholds)
                log.info(f"Fraud thresholds loaded: REVIEW={_thresholds['T_REVIEW']}, BLOCK={_thresholds['T_BLOCK']}")
        
        # Load feature names if available
        if os.path.exists(FEATURE_NAMES_PATH):
            with open(FEATURE_NAMES_PATH, "r") as f:
                _feature_names = json.load(f)
                log.info(f"Feature names loaded: {len(_feature_names)} features")
        
        return True
        
    except Exception as e:
        log.error(f"Error loading fraud detection model: {e}")
        return False


# ==============================================================================
# Feature Engineering Functions (from wissal_backend/IA/feature_builder.py)
# ==============================================================================

def entropy(s: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0.0
    probs = [freq / len(s) for freq in Counter(s).values()]
    return round(-sum(p * math.log2(p) for p in probs), 3)


def ratio_digits(s: str) -> float:
    """Ratio of digits in string."""
    return round(sum(c.isdigit() for c in s) / len(s), 3) if s else 0.0


def ratio_alpha(s: str) -> float:
    """Ratio of alphabetic characters in string."""
    return round(sum(c.isalpha() for c in s) / len(s), 3) if s else 0.0


def ratio_vowels(s: str) -> float:
    """Ratio of vowels in string."""
    return round(sum(c.lower() in "aeiouy" for c in s) / len(s), 3) if s else 0.0


def has_nonlatin(s: str) -> int:
    """Check if string contains non-Latin characters."""
    return int(any(ord(c) > 127 for c in s))


def is_blacklisted(s: str) -> int:
    """Check if string contains blacklisted words."""
    s_lower = s.lower()
    return int(any(bad in s_lower for bad in BLACKLIST))


def is_disposable(email: str) -> int:
    """Check if email uses a disposable domain."""
    domain = email.split("@")[-1].lower() if email and "@" in email else ""
    return int(domain in DISPOSABLE_DOMAINS)


def domain_known(email: str) -> int:
    """Check if email uses a known/trusted domain."""
    domain = email.split("@")[-1].lower() if email and "@" in email else ""
    return int(domain in KNOWN_DOMAINS)


def username_email_similarity(username: str, email: str) -> float:
    """Measure similarity between username and email local part."""
    if not username or not email or "@" not in email:
        return 0.0
    local = email.split("@")[0].lower()
    u = username.lower()
    common = sum(1 for c in u if c in local)
    return round(common / max(len(u), len(local)), 3)


def build_features(username: str, email: str, full_name: str, time_to_submit_ms: float = 60000.0) -> Dict:
    """
    Build feature dictionary from user signup data.
    
    Args:
        username: User's chosen username
        email: User's email address
        full_name: User's full name
        time_to_submit_ms: Time taken to submit form (not currently used)
    
    Returns:
        Dictionary of features matching the trained model's input
    """
    local = email.split("@")[0] if email and "@" in email else ""
    
    return {
        "is_disposable_domain": is_disposable(email),
        "is_known_domain": domain_known(email),
        "digits_ratio_local": ratio_digits(local),
        "local_entropy": entropy(local),
        "alpha_ratio": ratio_alpha(username) if username else 0.0,
        "vowel_ratio": ratio_vowels(full_name) if full_name else 0.0,
        "nonlatin_flag": has_nonlatin(full_name) if full_name else 0,
        "blacklist_hit": is_blacklisted(username) if username else 0,
        "username_length": len(username) if username else 0,
        "similarity_username_email": username_email_similarity(username, email)
    }


def score_signup(username: str, email: str, full_name: str, request_context: Optional[Dict] = None) -> Tuple[Optional[float], bool, str]:
    """
    Score a signup for fraud risk using the ML model.
    
    Args:
        username: User's username
        email: User's email
        full_name: User's full name
        request_context: Optional dict with IP, user-agent, etc. (future use)
    
    Returns:
        Tuple of (risk_score, is_suspicious, fraud_reason)
        - risk_score: 0.0 to 1.0 probability of fraud (None if model unavailable)
        - is_suspicious: True if score exceeds review threshold
        - fraud_reason: Human-readable explanation
    """
    global _model, _thresholds
    
    # If model not loaded, return safe defaults
    if _model is None:
        log.warning("Fraud model not available. Skipping fraud detection.")
        return (None, False, "model_unavailable")
    
    try:
        # Build features
        features = build_features(
            username=username or "",
            email=email or "",
            full_name=full_name or "",
            time_to_submit_ms=60000.0  # Default value
        )
        
        # Convert to DataFrame for sklearn
        X = pd.DataFrame([features])
        
        # Get prediction probability
        risk_score = float(_model.predict_proba(X)[0, 1])
        
        # Determine decision based on thresholds
        if risk_score >= _thresholds["T_BLOCK"]:
            decision = "auto-block-recommended"
            is_suspicious = True
        elif risk_score >= _thresholds["T_REVIEW"]:
            decision = "auto-review-required"
            is_suspicious = True
        else:
            decision = "auto-allow"
            is_suspicious = False
        
        log.info(f"Fraud score for {email}: {risk_score:.4f} (decision: {decision})")
        
        return (round(risk_score, 4), is_suspicious, decision)
        
    except Exception as e:
        log.error(f"Error scoring signup for {email}: {e}")
        # Fail open - don't block signup due to ML errors
        return (None, False, f"error: {str(e)[:50]}")


def get_fraud_stats() -> Dict:
    """Get fraud detection statistics."""
    stats = {
        "model_loaded": _model is not None,
        "model_path": MODEL_PATH if _model else None,
        "feature_count": len(_feature_names) if _feature_names else 0,
        "features": _feature_names if _feature_names else []
    }
    
    # Add threshold values
    if _thresholds:
        stats["T_REVIEW"] = _thresholds.get("T_REVIEW")
        stats["T_BLOCK"] = _thresholds.get("T_BLOCK")
        stats["thresholds"] = _thresholds
    
    return stats


# Initialize model on module import
load_model()

