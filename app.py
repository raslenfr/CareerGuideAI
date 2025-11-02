"""
GET /
    ➤ Health check endpoint.
    ➤ Returns service status, version, LLM availability, and available endpoints.

Response Example:
{
    "service": "Career Guidance API",
    "status": "Running",
    "version": "1.0.0",
    "llm_status": "Initialized",
    "endpoints": {
        "chatbot": "/api/chatbot/message (POST)",
        "suggester_start": "/api/suggester/start (GET)",
        "suggester_answer": "/api/suggester/answer (POST)",
        "recommender_start": "/api/recommender/start (POST)",
        "recommender_submit": "/api/recommender/submit (POST)"
    }
}
"""

import os
from flask_cors import CORS
from flask import Flask, jsonify
from dotenv import load_dotenv
import logging
from flask import request

# Load environment variables from .env file
load_dotenv()

# Import extensions
from extensions import db, bcrypt

# Import blueprints
from blueprints.chatbot_bp import chatbot_bp
from blueprints.suggester_bp import suggester_bp
from blueprints.recommender_bp import recommender_bp
from blueprints.auth_bp import auth_bp
from blueprints.admin_bp import admin_bp  # NEW: Admin panel
# Test/Diagnostic blueprints (for AI testing framework - can be removed in production if not needed)
from blueprints.test_reports_bp import test_reports_bp
from blueprints.test_recording_bp import test_recording_bp

# Configure basic logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
log = logging.getLogger(__name__) # Get logger for app context

app = Flask(__name__)

# ✅ Enable CORS for all routes (allow all origins for development)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": False
    }
})

# Load secret key for Flask session management (used implicitly by session)
# IMPORTANT: Use a strong, randomly generated key in production, set via environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    log.warning("FLASK_SECRET_KEY environment variable not set. Using default insecure key for development.")
    app.secret_key = "dev-secret-key-insecure" # Fallback for dev ONLY

# ✅ Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    log.info("Database tables created successfully.")

# Check if Groq key is loaded (for early warning)
from services.llm_service import client as llm_client
if llm_client is None:
    log.warning("Groq client is not initialized. LLM features will not work.")
else:
    log.info("Groq client is available and LLM features should work.")
# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)  # NEW: Admin panel
app.register_blueprint(chatbot_bp)
app.register_blueprint(suggester_bp)
app.register_blueprint(recommender_bp)
# Test/Diagnostic blueprints (for AI testing framework - can be removed in production if not needed)
app.register_blueprint(test_reports_bp)
app.register_blueprint(test_recording_bp)
log.info("✅ All blueprints registered successfully (including admin panel).")

# Basic root route / health check
@app.route('/')
def index():
    llm_status = "Initialized" if llm_client is not None else "Not Initialized (Check API Key)"
    return jsonify({
        "service": "Career Guidance API (Enhanced with Wissal Backend)",
        "status": "Running",
        "version": "2.0.0",
        "llm_status": llm_status,
        "database": "SQLite (course_recommendation.db)",
        "authentication": "JWT (Bearer tokens required)",
        "endpoints": {
            "auth_signup": "/api/auth/signup (POST) - Returns JWT",
            "auth_login": "/api/auth/login (POST) - Returns JWT",
            "auth_me": "/api/auth/me (GET) - Requires JWT",
            "auth_verify": "/api/auth/send-verification (POST) - Requires JWT",
            "auth_verify_email": "/api/auth/verify-email (POST) - Requires JWT",
            "admin_users": "/api/admin/users (GET) - Admin only",
            "admin_stats": "/api/admin/stats (GET) - Admin only",
            "chatbot": "/api/chatbot/message (POST) - Requires JWT",
            "suggester_start": "/api/suggester/start (GET)",
            "suggester_answer": "/api/suggester/answer (POST)",
            "recommender_start": "/api/recommender/start (POST)",
            "recommender_submit": "/api/recommender/submit (POST)"
        }
    })


# Generic error handlers
@app.errorhandler(404)
def not_found(error):
    log.warning(f"404 Not Found: {request.path}")
    return jsonify({"success": False, "error": "Not Found", "message": "The requested URL was not found on the server."}), 404

@app.errorhandler(500)
def internal_error(error):
    # Log the actual error stack trace for debugging
    log.exception("An internal server error occurred.") # Logs exception info
    return jsonify({"success": False, "error": "Internal Server Error", "message": "An unexpected error occurred on the server."}), 500

@app.errorhandler(400)
def bad_request(error):
    # Use the description from abort(400, description=...) if available
    description = getattr(error, 'description', "The browser (or proxy) sent a request that this server could not understand.")
    log.warning(f"400 Bad Request: {description} (Path: {request.path})")
    return jsonify({"success": False, "error": "Bad Request", "message": description}), 400

@app.errorhandler(405)
def method_not_allowed(error):
     log.warning(f"405 Method Not Allowed: {request.method} for {request.path}")
     return jsonify({"success": False, "error": "Method Not Allowed", "message": "The method is not allowed for the requested URL."}), 405


if __name__ == '__main__':
    # Set debug=True for development ONLY - provides debugger and auto-reload
    # Set debug=False for production
    # host='0.0.0.0' makes it accessible on your network (use '127.0.0.1' for local only)
    log.info("Starting Flask development server...")
    app.run(debug=True, host='127.0.0.1', port=5000)

