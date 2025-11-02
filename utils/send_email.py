"""
Email Sending Utility (from Wissal Backend - Enhanced)
======================================================
Sends emails via SMTP (Gmail)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

log = logging.getLogger(__name__)

# SMTP Configuration from environment variables
SMTP_SERVER = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "Career Guidance Platform")

if not SMTP_USERNAME or not SMTP_PASSWORD:
    log.warning("⚠️ SMTP credentials not set! Email sending will fail. Set SMTP_USERNAME and SMTP_PASSWORD in .env")


def send_email(to_email: str, subject: str, body: str, html_body: str = None):
    """
    Send an email via SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text body
        html_body: Optional HTML body (if provided, will send both plain and HTML)
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        log.error("Cannot send email: SMTP credentials not configured")
        return False
    
    try:
        if html_body:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
        else:
            msg = MIMEText(body, "plain")
        
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USERNAME}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            log.info(f"✅ Email sent to {to_email}")
            return True
            
    except Exception as e:
        log.error(f"❌ Error sending email to {to_email}: {e}")
        return False

