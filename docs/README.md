🎓 CareerGuide AI - Backend System
A comprehensive Flask backend that provides personalized career guidance, course recommendations, and AI-powered career advice. The system uses Large Language Models (LLaMA3 via Groq) combined with structured data to deliver accurate, Tunisia-focused guidance for career development and learning paths.

🏗️ Project Structure
text

<table> <thead> <tr> <th>Folder/File</th> <th>Type</th> <th>Description</th> </tr> </thead> <tbody> <tr> <td><strong>Backend/</strong></td> <td>Folder</td> <td>Root backend directory</td> </tr> <tr> <td style="padding-left: 30px;">app.py</td> <td>File</td> <td>Flask application entrypoint</td> </tr> <tr> <td style="padding-left: 30px;">extensions.py</td> <td>File</td> <td>SQLAlchemy & Bcrypt initialization</td> </tr> <tr> <td style="padding-left: 30px;">models.py</td> <td>File</td> <td>Database models (User, ChatHistory, etc.)</td> </tr> <tr> <td style="padding-left: 30px;"><strong>blueprints/</strong></td> <td>Folder</td> <td>API route blueprints</td> </tr> <tr> <td style="padding-left: 60px;">auth_bp.py</td> <td>File</td> <td>Authentication endpoints</td> </tr> <tr> <td style="padding-left: 60px;">chatbot_bp.py</td> <td>File</td> <td>Chatbot with history management</td> </tr> <tr> <td style="padding-left: 60px;">suggester_bp.py</td> <td>File</td> <td>Career suggester with sessions</td> </tr> <tr> <td style="padding-left: 60px;">recommender_bp.py</td> <td>File</td> <td>Course recommender</td> </tr> <tr> <td style="padding-left: 60px;">test_reports_bp.py</td> <td>File</td> <td>Test report API</td> </tr> <tr> <td style="padding-left: 60px;">test_recording_bp.py</td> <td>File</td> <td>Real-time test recording</td> </tr> <tr> <td style="padding-left: 60px;">admin_bp.py</td> <td>File</td> <td>Admin interface endpoints</td> </tr> <tr> <td style="padding-left: 30px;"><strong>services/</strong></td> <td>Folder</td> <td>Business logic services</td> </tr> <tr> <td style="padding-left: 60px;">llm_service.py</td> <td>File</td> <td>LLM integration (Groq/LLaMA3)</td> </tr> <tr> <td style="padding-left: 60px;">job_search_service.py</td> <td>File</td> <td>Static job/course data</td> </tr> <tr> <td style="padding-left: 60px;">fraud_detection_service.py</td> <td>File</td> <td>ML-powered fraud detection</td> </tr> <tr> <td style="padding-left: 30px;"><strong>tests/</strong></td> <td>Folder</td> <td>AI testing framework</td> </tr> <tr> <td style="padding-left: 60px;">diagnostic_framework.py</td> <td>File</td> <td>Testing framework base classes</td> </tr> <tr> <td style="padding-left: 60px;">test_chatbot.py</td> <td>File</td> <td>Chatbot AI tests</td> </tr> <tr> <td style="padding-left: 60px;">test_career_suggester.py</td> <td>File</td> <td>Career suggester tests</td> </tr> <tr> <td style="padding-left: 60px;">test_course_recommender.py</td> <td>File</td> <td>Course recommender tests</td> </tr> <tr> <td style="padding-left: 30px;">run_ai_tests.py</td> <td>File</td> <td>CLI test runner</td> </tr> <tr> <td style="padding-left: 30px;"><strong>logs/</strong></td> <td>Folder</td> <td>AI diagnostic reports (JSON)</td> </tr> <tr> <td style="padding-left: 30px;"><strong>instance/</strong></td> <td>Folder</td> <td>Database instance</td> </tr> <tr> <td style="padding-left: 60px;">course_recommendation.db</td> <td>File</td> <td>SQLite database</td> </tr> <tr> <td style="padding-left: 30px;">.env</td> <td>File</td> <td>Environment variables</td> </tr> <tr> <td style="padding-left: 30px;">requirements.txt</td> <td>File</td> <td>Python dependencies</td> </tr> <tr> <td style="padding-left: 30px;">README.md</td> <td>File</td> <td>Backend documentation</td> </tr> </tbody> </table>

✨ Features
Core AI Features
🤖 AI Career Chatbot - Real-time conversational career advice with chat history

📋 Career Suggester - 11-question assessment for personalized career path recommendations

🔍 Course Recommender - Survey-based course recommendations with filtering

💾 Chat History Management - Save, load, update, and delete conversations

💼 Session Management - Save and revisit career assessment sessions

Authentication & Database
🔐 User Authentication - Secure signup/login with password hashing (Flask-Bcrypt)

🗄️ SQLite Database - Persistent storage for users, chat history, and career suggestions

👤 User Profiles - Track individual user progress and saved data

🛡️ Role-Based Access Control - Admin and student roles with protected endpoints

🛡️ Admin Interface Features
👥 User Management - View, search, update, and delete user accounts

📊 Platform Statistics - Comprehensive dashboard with user analytics

🛡️ Fraud Detection System - ML-powered risk scoring for suspicious signups

📝 Audit Logs - Complete action history and activity tracking

🔍 Fraud Queue - Review and take action on suspicious accounts

✅ Manual Email Verification - Verify user emails without email process

AI Testing & Quality Assurance
🧪 Integrated Testing - Real-time AI interaction recording and analysis

📊 Detailed Test Reports - Comprehensive quality reports with scores, issues, and metrics

🎯 Automatic AI Detection - Smart detection of which AI component is being tested

📈 Performance Metrics - Response time tracking and quality scoring

🔍 CLI Test Runner - Command-line tools for automated AI diagnostics

📁 JSON Report Export - Timestamped diagnostic logs saved to logs/

🔌 API Endpoints
AUTHENTICATION
POST /api/auth/signup - Register new user

POST /api/auth/login - Authenticate user

CHATBOT
POST /api/chatbot/message - Send message and get AI response

GET /api/chatbot/conversations - List user's saved conversations

GET /api/chatbot/conversations/<id> - Load specific conversation

DELETE /api/chatbot/conversations/<id> - Delete conversation

POST /api/chatbot/save-conversation - Save/update conversation

CAREER SUGGESTER
GET /api/suggester/start - Start new assessment

POST /api/suggester/answer - Submit answer, get next question

GET /api/suggester/sessions - List saved sessions

GET /api/suggester/sessions/<id> - Load specific session

DELETE /api/suggester/sessions/<id> - Delete session

POST /api/suggester/save-session - Save completed assessment

COURSE RECOMMENDER
POST /api/recommender/start - Initialize course search

POST /api/recommender/submit - Submit survey, get recommendations

ADMIN INTERFACE
GET /api/admin/users - List all users with search and pagination

GET /api/admin/users/<id> - Get specific user details

PUT /api/admin/users/<id> - Update user information

DELETE /api/admin/users/<id> - Delete user account

POST /api/admin/users/<id>/verify - Manually verify user email

GET /api/admin/stats - Get platform statistics

GET /api/admin/logs - Get audit logs

GET /api/admin/fraud/queue - Get fraud detection queue

POST /api/admin/fraud/review - Review and take action on suspicious user

AI TESTING
POST /api/tests/start-recording - Start test recording session

POST /api/tests/log-interaction - Log AI interaction

POST /api/tests/stop-recording - Stop recording, generate report

GET /api/tests/session-status/<id> - Get recording session status

GET /api/tests/reports - List all test reports

GET /api/tests/reports/<id> - Get specific report details

GET /api/tests/reports/stats - Get aggregate test statistics

GENERAL
GET / - Health check and endpoint list

🚀 Setup Instructions
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/YourUsername/course-recommendation.git
cd course-recommendation-main/Backend
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Environment Configuration
Create a .env file in the Backend directory:

env
FLASK_SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
Initialize Database
The database will be automatically created when you first run the application.

Run the backend

bash
python app.py
Backend runs on http://localhost:5000

📦 Dependencies
Core Backend
Flask>=2.0 - Web framework

Flask-CORS>=3.0.10 - CORS support

Flask-SQLAlchemy>=3.0.0 - Database ORM

Flask-Bcrypt>=1.0.1 - Password hashing

AI & ML Services
groq>=0.22.0 - LLM API client

scikit-learn>=1.0 - ML for fraud detection

pandas>=1.5 - Data processing

Utilities
python-dotenv>=0.15 - Environment variables

requests>=2.25 - HTTP requests

🧪 AI Testing System
Running Diagnostic Tests (CLI)
Test all AI components:

bash
python run_ai_tests.py --verbose
Test specific AI components:

bash
python run_ai_tests.py --test chatbot --verbose
python run_ai_tests.py --test career_suggester --verbose
python run_ai_tests.py --test course_recommender --verbose
View saved reports:

bash
python tests/report_viewer.py --list
python tests/report_viewer.py --report <filename>
python tests/report_viewer.py --stats
Test Report Structure
Test reports are saved as JSON files in the logs/ directory with comprehensive analysis including:

Overall AI performance scores (0-100)

Individual interaction analysis

Response time metrics

Quality assessment

Issues and recommendations

🛡️ Fraud Detection System
How It Works
The system automatically analyzes user signups using machine learning:

Risk Scoring: ML model calculates fraud risk from 0.0 (low) to 1.0 (high)

Feature Analysis: Examines 10 different features including email domains, username patterns, and name characteristics

Automatic Flagging: Flags accounts based on risk thresholds

Manual Review: All suspicious accounts go to admin review queue

Risk Categories
Low Risk (score < 0.4): Automatically allowed

Medium Risk (0.4 - 0.8): Flagged for manual review

High Risk (score ≥ 0.8): Recommended for blocking

Admin Review Actions
✅ Verify as Legitimate: Mark safe and verify email

🚫 Block Account: Permanently disable fraudulent accounts

🔄 Clear Flag: Remove suspicion for false positives

📊 Database Schema
Users Table
sql
id: Integer (Primary Key)
username: String(80), unique
email: String(120), unique
password_hash: String(128)
role: String(20)  # 'admin' or 'student'
is_verified: Boolean
fraud_risk_score: Float
fraud_reason: String
review_status: String  # 'pending', 'reviewed', 'cleared'
created_at: DateTime
ChatHistory Table
sql
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
conversation_id: String
chat_title: String
role: String  # 'user' or 'assistant'
message: Text
created_at: DateTime
CareerSuggestion Table
sql
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
session_id: String
session_title: String
answers: JSON  # Store assessment answers
suggestions: JSON  # Store career suggestions
created_at: DateTime
AuditLogs Table
sql
id: Integer (Primary Key)
admin_id: Integer (Foreign Key)
action_type: String  # 'delete_user', 'update_user', 'verify_user', etc.
target_user_id: Integer
notes: Text
timestamp: DateTime
🎯 Example API Requests
User Registration
bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
Chatbot Interaction
bash
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What career paths are available in Tunisia for IT graduates?",
    "user_id": 1,
    "conversation_id": "uuid-here"
  }'
Career Assessment
bash
curl -X POST http://localhost:5000/api/suggester/answer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid",
    "question_id": 1,
    "answer": "Technology"
  }'
🔒 Security Features
Password Hashing: Bcrypt for secure password storage

CORS Configuration: Proper cross-origin resource sharing settings

SQL Injection Prevention: SQLAlchemy ORM with parameterized queries

Environment Variables: Sensitive data protection

Role-Based Access: Admin and student role enforcement

Audit Logging: Complete action tracking for compliance

JWT Authentication: Secure token-based authentication

🌍 Tunisia Localization
All career guidance and recommendations are specifically tailored for the Tunisian market:

Local job market insights

Tunisia-specific career paths

Local education and certification recommendations

Regional industry focus

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License.

🙏 Acknowledgments
LLM Provider: Groq (LLaMA3-8B model)

Backend Framework: Flask

Database: SQLite with SQLAlchemy ORM

ML Framework: Scikit-learn for fraud detection

📧 Support
For technical support or questions about the backend system, please open an issue on GitHub.

Built with ❤️ for the Tunisian tech community

