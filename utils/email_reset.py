"""
Password Reset Email Utility (from Wissal Backend)
==================================================
Sends password reset codes
"""

import random
from utils.send_email import send_email
import logging

log = logging.getLogger(__name__)


def generate_reset_code():
    """Generate a 6-digit password reset code."""
    return str(random.randint(100000, 999999))


def send_reset_code(to_email: str, username: str, code: str):
    """
    Send password reset code via email.
    
    Args:
        to_email: Recipient email
        username: User's name
        code: 6-digit reset code
    
    Returns:
        True if sent successfully
    """
    subject = "🔐 Password Reset Request"
    
    body_plain = f"""
Hello {username},

You requested to reset your password. Use the following code to proceed:

Code: {code}

This code is valid for 10 minutes.

If you didn't request a password reset, please ignore this email or contact support if you have concerns.

Best regards,
Career Guidance Team
    """
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
          <h2 style="color:#FF5722; margin-bottom:20px;">Password Reset Request</h2>
          <p style="color:#555; font-size:16px;">Hello <strong>{username}</strong>,</p>
          <p style="color:#555; font-size:16px;">You requested to reset your password. Use the following code to proceed:</p>
          
          <div style="background:#fff3e0; padding:15px; border-radius:5px; border-left:4px solid #FF5722; margin:20px 0;">
            <p style="color:#333; font-size:14px; margin:0;">Your reset code:</p>
            <span style="font-size:32px; font-weight:bold; color:#FF5722; letter-spacing:5px; display:block; text-align:center; margin:10px 0;">{code}</span>
          </div>
          
          <p style="color:#888; font-size:14px;">⏱️ This code is valid for <strong>10 minutes</strong>.</p>
          
          <div style="background:#f8f9fa; padding:15px; border-radius:5px; margin:20px 0;">
            <p style="color:#666; font-size:14px; margin:0;">
              ⚠️ If you didn't request a password reset, please ignore this email or contact support if you have concerns.
            </p>
          </div>
          
          <hr style="border:none; border-top:1px solid #eee; margin:30px 0;">
          <p style="color:#aaa; font-size:12px; text-align:center;">Career Guidance Platform - Security Team</p>
        </div>
      </body>
    </html>
    """
    
    result = send_email(to_email, subject, body_plain, body_html)
    
    if result:
        log.info(f"Password reset code sent to {to_email}")
    else:
        log.error(f"Failed to send password reset code to {to_email}")
    
    return result

