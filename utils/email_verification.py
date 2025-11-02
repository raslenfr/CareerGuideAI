"""
Email Verification Utility (from Wissal Backend)
================================================
Generates and sends 6-digit verification codes
"""

import random
import string
from utils.send_email import send_email
import logging

log = logging.getLogger(__name__)


def generate_code(length=6):
    """
    Generate a random numeric verification code.
    
    Args:
        length: Length of code (default 6 digits)
    
    Returns:
        String of random digits
    """
    return ''.join(random.choices(string.digits, k=length))


def send_verification_code(to_email: str, code: str, username: str = "User"):
    """
    Send email verification code.
    
    Args:
        to_email: Recipient email
        code: 6-digit verification code
        username: User's name for personalization
    
    Returns:
        True if sent successfully
    """
    subject = "🔐 Email Verification Code"
    
    body_plain = f"""
Hello {username},

Your email verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Career Guidance Team
    """
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
          <h2 style="color:#2C3E50; margin-bottom:20px;">Email Verification</h2>
          <p style="color:#555; font-size:16px;">Hello <strong>{username}</strong>,</p>
          <p style="color:#555; font-size:16px;">Your email verification code is:</p>
          <div style="background:#f8f9fa; padding:15px; border-radius:5px; text-align:center; margin:20px 0;">
            <span style="font-size:32px; font-weight:bold; color:#4CAF50; letter-spacing:5px;">{code}</span>
          </div>
          <p style="color:#888; font-size:14px;">This code will expire in 10 minutes.</p>
          <p style="color:#888; font-size:14px;">If you didn't request this code, please ignore this email.</p>
          <hr style="border:none; border-top:1px solid #eee; margin:30px 0;">
          <p style="color:#aaa; font-size:12px; text-align:center;">Career Guidance Platform</p>
        </div>
      </body>
    </html>
    """
    
    result = send_email(to_email, subject, body_plain, body_html)
    
    if result:
        log.info(f"Verification code sent to {to_email}")
    else:
        log.error(f"Failed to send verification code to {to_email}")
    
    return result

