"""
Welcome Email Utility (from Wissal Backend)
===========================================
Sends welcome emails to new users
"""

from utils.send_email import send_email
import logging

log = logging.getLogger(__name__)


def send_welcome_email(to_email: str, username: str):
    """
    Send welcome email to new users.
    
    Args:
        to_email: Recipient email
        username: User's name
    
    Returns:
        True if sent successfully
    """
    subject = "🎉 Welcome to Career Guidance Platform!"
    
    body_plain = f"""
Hello {username},

Welcome to the Career Guidance Platform! 🎓

We're thrilled to have you join our community. You can now explore:

• AI-Powered Career Chatbot - Get personalized career advice
• Career Path Suggester - Discover careers that match your skills
• Course Recommendations - Find the perfect courses for your goals

Get started now by logging in to your account.

If you have any questions, feel free to reach out to our support team.

Best regards,
The Career Guidance Team
    """
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
          <h1 style="color:#4CAF50; text-align:center; margin-bottom:10px;">Welcome! 🎉</h1>
          <p style="color:#555; font-size:18px; text-align:center;">Hello <strong>{username}</strong>,</p>
          <p style="color:#666; font-size:16px; line-height:1.6;">
            We're thrilled to have you join our Career Guidance Platform! 🎓
          </p>
          
          <div style="background:#f8f9fa; padding:20px; border-radius:5px; margin:20px 0;">
            <h3 style="color:#333; margin-top:0;">What You Can Do:</h3>
            <ul style="color:#555; line-height:1.8;">
              <li><strong>AI Career Chatbot</strong> - Get personalized career advice</li>
              <li><strong>Career Path Suggester</strong> - Discover careers that match your skills</li>
              <li><strong>Course Recommendations</strong> - Find the perfect courses for your goals</li>
            </ul>
          </div>
          
          <div style="text-align:center; margin:30px 0;">
            <a href="http://localhost:3000/login" 
               style="display:inline-block; padding:12px 30px; background:#4CAF50; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">
              Get Started
            </a>
          </div>
          
          <p style="color:#888; font-size:14px; text-align:center; margin-top:30px;">
            If you have any questions, feel free to reach out to our support team.
          </p>
          
          <hr style="border:none; border-top:1px solid #eee; margin:30px 0;">
          <p style="color:#aaa; font-size:12px; text-align:center;">
            Career Guidance Platform<br>
            Empowering Your Career Journey
          </p>
        </div>
      </body>
    </html>
    """
    
    result = send_email(to_email, subject, body_plain, body_html)
    
    if result:
        log.info(f"Welcome email sent to {to_email}")
    else:
        log.error(f"Failed to send welcome email to {to_email}")
    
    return result

