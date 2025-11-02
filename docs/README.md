# 🎓 CareerGuide AI - Backend System

A comprehensive Flask backend that provides personalized career guidance, course recommendations, and AI-powered career advice. The system uses Large Language Models (LLaMA3 via Groq) combined with structured data to deliver accurate, Tunisia-focused guidance for career development and learning paths.

## 🏗️ Project Structure

<table>
<thead>
<tr>
<th>Folder/File</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Backend/</strong></td>
<td>Folder</td>
<td>Root backend directory</td>
</tr>
<tr>
<td style="padding-left: 30px;">app.py</td>
<td>File</td>
<td>Flask application entrypoint</td>
</tr>
<tr>
<td style="padding-left: 30px;">extensions.py</td>
<td>File</td>
<td>SQLAlchemy & Bcrypt initialization</td>
</tr>
<tr>
<td style="padding-left: 30px;">models.py</td>
<td>File</td>
<td>Database models (User, ChatHistory, etc.)</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>blueprints/</strong></td>
<td>Folder</td>
<td>API route blueprints</td>
</tr>
<tr>
<td style="padding-left: 60px;">auth_bp.py</td>
<td>File</td>
<td>Authentication endpoints</td>
</tr>
<tr>
<td style="padding-left: 60px;">chatbot_bp.py</td>
<td>File</td>
<td>Chatbot with history management</td>
</tr>
<tr>
<td style="padding-left: 60px;">suggester_bp.py</td>
<td>File</td>
<td>Career suggester with sessions</td>
</tr>
<tr>
<td style="padding-left: 60px;">recommender_bp.py</td>
<td>File</td>
<td>Course recommender</td>
</tr>
<tr>
<td style="padding-left: 60px;">test_reports_bp.py</td>
<td>File</td>
<td>Test report API</td>
</tr>
<tr>
<td style="padding-left: 60px;">test_recording_bp.py</td>
<td>File</td>
<td>Real-time test recording</td>
</tr>
<tr>
<td style="padding-left: 60px;">admin_bp.py</td>
<td>File</td>
<td>Admin interface endpoints</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>services/</strong></td>
<td>Folder</td>
<td>Business logic services</td>
</tr>
<tr>
<td style="padding-left: 60px;">llm_service.py</td>
<td>File</td>
<td>LLM integration (Groq/LLaMA3)</td>
</tr>
<tr>
<td style="padding-left: 60px;">job_search_service.py</td>
<td>File</td>
<td>Static job/course data</td>
</tr>
<tr>
<td style="padding-left: 60px;">fraud_detection_service.py</td>
<td>File</td>
<td>ML-powered fraud detection</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>tests/</strong></td>
<td>Folder</td>
<td>AI testing framework</td>
</tr>
<tr>
<td style="padding-left: 60px;">diagnostic_framework.py</td>
<td>File</td>
<td>Testing framework base classes</td>
</tr>
<tr>
<td style="padding-left: 60px;">test_chatbot.py</td>
<td>File</td>
<td>Chatbot AI tests</td>
</tr>
<tr>
<td style="padding-left: 60px;">test_career_suggester.py</td>
<td>File</td>
<td>Career suggester tests</td>
</tr>
<tr>
<td style="padding-left: 60px;">test_course_recommender.py</td>
<td>File</td>
<td>Course recommender tests</td>
</tr>
<tr>
<td style="padding-left: 30px;">run_ai_tests.py</td>
<td>File</td>
<td>CLI test runner</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>logs/</strong></td>
<td>Folder</td>
<td>AI diagnostic reports (JSON)</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>instance/</strong></td>
<td>Folder</td>
<td>Database instance</td>
</tr>
<tr>
<td style="padding-left: 60px;">course_recommendation.db</td>
<td>File</td>
<td>SQLite database</td>
</tr>
<tr>
<td style="padding-left: 30px;">.env</td>
<td>File</td>
<td>Environment variables</td>
</tr>
<tr>
<td style="padding-left: 30px;">requirements.txt</td>
<td>File</td>
<td>Python dependencies</td>
</tr>
<tr>
<td style="padding-left: 30px;">README.md</td>
<td>File</td>
<td>Backend documentation</td>
</tr>
</tbody>
</table>

## ✨ Features

<table>
<thead>
<tr>
<th>Category</th>
<th>Feature</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="5"><strong>Core AI Features</strong></td>
<td>🤖 AI Career Chatbot</td>
<td>Real-time conversational career advice with chat history</td>
</tr>
<tr>
<td>📋 Career Suggester</td>
<td>11-question assessment for personalized career path recommendations</td>
</tr>
<tr>
<td>🔍 Course Recommender</td>
<td>Survey-based course recommendations with filtering</td>
</tr>
<tr>
<td>💾 Chat History Management</td>
<td>Save, load, update, and delete conversations</td>
</tr>
<tr>
<td>💼 Session Management</td>
<td>Save and revisit career assessment sessions</td>
</tr>
<tr>
<td rowspan="3"><strong>Authentication & Database</strong></td>
<td>🔐 User Authentication</td>
<td>Secure signup/login with password hashing (Flask-Bcrypt)</td>
</tr>
<tr>
<td>🗄️ SQLite Database</td>
<td>Persistent storage for users, chat history, and career suggestions</td>
</tr>
<tr>
<td>👤 User Profiles</td>
<td>Track individual user progress and saved data</td>
</tr>
<tr>
<td rowspan="6"><strong>Admin Interface</strong></td>
<td>👥 User Management</td>
<td>View, search, update, and delete user accounts</td>
</tr>
<tr>
<td>📊 Platform Statistics</td>
<td>Comprehensive dashboard with user analytics</td>
</tr>
<tr>
<td>🛡️ Fraud Detection System</td>
<td>ML-powered risk scoring for suspicious signups</td>
</tr>
<tr>
<td>📝 Audit Logs</td>
<td>Complete action history and activity tracking</td>
</tr>
<tr>
<td>🔍 Fraud Queue</td>
<td>Review and take action on suspicious accounts</td>
</tr>
<tr>
<td>✅ Manual Email Verification</td>
<td>Verify user emails without email process</td>
</tr>
<tr>
<td rowspan="6"><strong>AI Testing & QA</strong></td>
<td>🧪 Integrated Testing</td>
<td>Real-time AI interaction recording and analysis</td>
</tr>
<tr>
<td>📊 Detailed Test Reports</td>
<td>Comprehensive quality reports with scores, issues, and metrics</td>
</tr>
<tr>
<td>🎯 Automatic AI Detection</td>
<td>Smart detection of which AI component is being tested</td>
</tr>
<tr>
<td>📈 Performance Metrics</td>
<td>Response time tracking and quality scoring</td>
</tr>
<tr>
<td>🔍 CLI Test Runner</td>
<td>Command-line tools for automated AI diagnostics</td>
</tr>
<tr>
<td>📁 JSON Report Export</td>
<td>Timestamped diagnostic logs saved to logs/</td>
</tr>
</tbody>
</table>

## 🔌 API Endpoints

<table>
<thead>
<tr>
<th>Category</th>
<th>Endpoint</th>
<th>Method</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2"><strong>Authentication</strong></td>
<td><code>/api/auth/signup</code></td>
<td>POST</td>
<td>Register new user</td>
</tr>
<tr>
<td><code>/api/auth/login</code></td>
<td>POST</td>
<td>Authenticate user</td>
</tr>
<tr>
<td rowspan="5"><strong>Chatbot</strong></td>
<td><code>/api/chatbot/message</code></td>
<td>POST</td>
<td>Send message and get AI response</td>
</tr>
<tr>
<td><code>/api/chatbot/conversations</code></td>
<td>GET</td>
<td>List user's saved conversations</td>
</tr>
<tr>
<td><code>/api/chatbot/conversations/&lt;id&gt;</code></td>
<td>GET</td>
<td>Load specific conversation</td>
</tr>
<tr>
<td><code>/api/chatbot/conversations/&lt;id&gt;</code></td>
<td>DELETE</td>
<td>Delete conversation</td>
</tr>
<tr>
<td><code>/api/chatbot/save-conversation</code></td>
<td>POST</td>
<td>Save/update conversation</td>
</tr>
<tr>
<td rowspan="6"><strong>Career Suggester</strong></td>
<td><code>/api/suggester/start</code></td>
<td>GET</td>
<td>Start new assessment</td>
</tr>
<tr>
<td><code>/api/suggester/answer</code></td>
<td>POST</td>
<td>Submit answer, get next question</td>
</tr>
<tr>
<td><code>/api/suggester/sessions</code></td>
<td>GET</td>
<td>List saved sessions</td>
</tr>
<tr>
<td><code>/api/suggester/sessions/&lt;id&gt;</code></td>
<td>GET</td>
<td>Load specific session</td>
</tr>
<tr>
<td><code>/api/suggester/sessions/&lt;id&gt;</code></td>
<td>DELETE</td>
<td>Delete session</td>
</tr>
<tr>
<td><code>/api/suggester/save-session</code></td>
<td>POST</td>
<td>Save completed assessment</td>
</tr>
<tr>
<td rowspan="2"><strong>Course Recommender</strong></td>
<td><code>/api/recommender/start</code></td>
<td>POST</td>
<td>Initialize course search</td>
</tr>
<tr>
<td><code>/api/recommender/submit</code></td>
<td>POST</td>
<td>Submit survey, get recommendations</td>
</tr>
<tr>
<td rowspan="8"><strong>Admin Interface</strong></td>
<td><code>/api/admin/users</code></td>
<td>GET</td>
<td>List all users with search and pagination</td>
</tr>
<tr>
<td><code>/api/admin/users/&lt;id&gt;</code></td>
<td>GET</td>
<td>Get specific user details</td>
</tr>
<tr>
<td><code>/api/admin/users/&lt;id&gt;</code></td>
<td>PUT</td>
<td>Update user information</td>
</tr>
<tr>
<td><code>/api/admin/users/&lt;id&gt;</code></td>
<td>DELETE</td>
<td>Delete user account</td>
</tr>
<tr>
<td><code>/api/admin/users/&lt;id&gt;/verify</code></td>
<td>POST</td>
<td>Manually verify user email</td>
</tr>
<tr>
<td><code>/api/admin/stats</code></td>
<td>GET</td>
<td>Get platform statistics</td>
</tr>
<tr>
<td><code>/api/admin/logs</code></td>
<td>GET</td>
<td>Get audit logs</td>
</tr>
<tr>
<td><code>/api/admin/fraud/queue</code></td>
<td>GET</td>
<td>Get fraud detection queue</td>
</tr>
<tr>
<td rowspan="7"><strong>AI Testing</strong></td>
<td><code>/api/tests/start-recording</code></td>
<td>POST</td>
<td>Start test recording session</td>
</tr>
<tr>
<td><code>/api/tests/log-interaction</code></td>
<td>POST</td>
<td>Log AI interaction</td>
</tr>
<tr>
<td><code>/api/tests/stop-recording</code></td>
<td>POST</td>
<td>Stop recording, generate report</td>
</tr>
<tr>
<td><code>/api/tests/session-status/&lt;id&gt;</code></td>
<td>GET</td>
<td>Get recording session status</td>
</tr>
<tr>
<td><code>/api/tests/reports</code></td>
<td>GET</td>
<td>List all test reports</td>
</tr>
<tr>
<td><code>/api/tests/reports/&lt;id&gt;</code></td>
<td>GET</td>
<td>Get specific report details</td>
</tr>
<tr>
<td><code>/api/tests/reports/stats</code></td>
<td>GET</td>
<td>Get aggregate test statistics</td>
</tr>
<tr>
<td><strong>General</strong></td>
<td><code>/</code></td>
<td>GET</td>
<td>Health check and endpoint list</td>
</tr>
</tbody>
</table>

## 🚀 Setup Instructions

<table>
<thead>
<tr>
<th>Step</th>
<th>Command</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Clone Repository</td>
<td><code>git clone https://github.com/YourUsername/course-recommendation.git</code></td>
<td>Clone the project repository</td>
</tr>
<tr>
<td>2. Navigate to Backend</td>
<td><code>cd course-recommendation-main/Backend</code></td>
<td>Enter backend directory</td>
</tr>
<tr>
<td>3. Create Virtual Environment</td>
<td><code>python -m venv venv</code></td>
<td>Create Python virtual environment</td>
</tr>
<tr>
<td>4. Activate Environment</td>
<td><code>source venv/bin/activate</code><br><em>(Windows: <code>venv\Scripts\activate</code>)</em></td>
<td>Activate the virtual environment</td>
</tr>
<tr>
<td>5. Install Dependencies</td>
<td><code>pip install -r requirements.txt</code></td>
<td>Install all Python dependencies</td>
</tr>
<tr>
<td>6. Environment Setup</td>
<td>Create <code>.env</code> file with required variables</td>
<td>Configure environment settings</td>
</tr>
<tr>
<td>7. Run Backend</td>
<td><code>python app.py</code></td>
<td>Start the Flask development server</td>
</tr>
</tbody>
</table>

### Environment Variables (.env)
<table>
<thead>
<tr>
<th>Variable</th>
<th>Description</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>FLASK_SECRET_KEY</code></td>
<td>Secret key for Flask session security</td>
<td><code>your_secret_key_here</code></td>
</tr>
<tr>
<td><code>GROQ_API_KEY</code></td>
<td>API key for Groq LLM service</td>
<td><code>gsk_...your_groq_api_key</code></td>
</tr>
</tbody>
</table>

## 📦 Dependencies

<table>
<thead>
<tr>
<th>Package</th>
<th>Version</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Flask</code></td>
<td>>=2.0</td>
<td>Web framework</td>
</tr>
<tr>
<td><code>Flask-CORS</code></td>
<td>>=3.0.10</td>
<td>CORS support</td>
</tr>
<tr>
<td><code>Flask-SQLAlchemy</code></td>
<td>>=3.0.0</td>
<td>Database ORM</td>
</tr>
<tr>
<td><code>Flask-Bcrypt</code></td>
<td>>=1.0.1</td>
<td>Password hashing</td>
</tr>
<tr>
<td><code>groq</code></td>
<td>>=0.22.0</td>
<td>LLM API client</td>
</tr>
<tr>
<td><code>scikit-learn</code></td>
<td>>=1.0</td>
<td>ML for fraud detection</td>
</tr>
<tr>
<td><code>pandas</code></td>
<td>>=1.5</td>
<td>Data processing</td>
</tr>
<tr>
<td><code>python-dotenv</code></td>
<td>>=0.15</td>
<td>Environment variables</td>
</tr>
<tr>
<td><code>requests</code></td>
<td>>=2.25</td>
<td>HTTP requests</td>
</tr>
</tbody>
</table>

## 🛡️ Fraud Detection System

<table>
<thead>
<tr>
<th>Risk Level</th>
<th>Score Range</th>
<th>Action</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>🟢 Low Risk</td>
<td>0.0 - 0.4</td>
<td>Auto-Allow</td>
<td>Account automatically approved</td>
</tr>
<tr>
<td>🟡 Medium Risk</td>
<td>0.4 - 0.8</td>
<td>Flag for Review</td>
<td>Sent to admin review queue</td>
</tr>
<tr>
<td>🔴 High Risk</td>
<td>0.8 - 1.0</td>
<td>Recommend Block</td>
<td>Suggested for account blocking</td>
</tr>
</tbody>
</table>

### Admin Review Actions
<table>
<thead>
<tr>
<th>Action</th>
<th>Icon</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Verify as Legitimate</td>
<td>✅</td>
<td>Mark safe and verify email automatically</td>
</tr>
<tr>
<td>Block Account</td>
<td>🚫</td>
<td>Permanently disable fraudulent account</td>
</tr>
<tr>
<td>Clear Flag</td>
<td>🔄</td>
<td>Remove suspicion for false positives</td>
</tr>
</tbody>
</table>

## 🧪 AI Testing Commands

<table>
<thead>
<tr>
<th>Command</th>
<th>Description</th>
<th>Output</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>python run_ai_tests.py --verbose</code></td>
<td>Test all AI components with detailed output</td>
<td>Comprehensive test report</td>
</tr>
<tr>
<td><code>python run_ai_tests.py --test chatbot</code></td>
<td>Test only chatbot functionality</td>
<td>Chatbot-specific metrics</td>
</tr>
<tr>
<td><code>python run_ai_tests.py --test career_suggester</code></td>
<td>Test career assessment system</td>
<td>Career suggester performance</td>
</tr>
<tr>
<td><code>python run_ai_tests.py --test course_recommender</code></td>
<td>Test course recommendation engine</td>
<td>Course recommender analysis</td>
</tr>
<tr>
<td><code>python tests/report_viewer.py --list</code></td>
<td>List all saved test reports</td>
<td>Report filenames and dates</td>
</tr>
<tr>
<td><code>python tests/report_viewer.py --report &lt;filename&gt;</code></td>
<td>View specific test report</td>
<td>Detailed JSON report data</td>
</tr>
<tr>
<td><code>python tests/report_viewer.py --stats</code></td>
<td>Show test statistics overview</td>
<td>Aggregate performance metrics</td>
</tr>
</tbody>
</table>

## 🔒 Security Features

<table>
<thead>
<tr>
<th>Feature</th>
<th>Technology</th>
<th>Benefit</th>
</tr>
</thead>
<tbody>
<tr>
<td>Password Hashing</td>
<td>Flask-Bcrypt</td>
<td>Secure password storage</td>
</tr>
<tr>
<td>CORS Protection</td>
<td>Flask-CORS</td>
<td>Cross-origin request security</td>
</tr>
<tr>
<td>SQL Injection Prevention</td>
<td>SQLAlchemy ORM</td>
<td>Parameterized query safety</td>
</tr>
<tr>
<td>Environment Security</td>
<td>python-dotenv</td>
<td>Sensitive data protection</td>
</tr>
<tr>
<td>Role-Based Access</td>
<td>Custom implementation</td>
<td>Admin/student role enforcement</td>
</tr>
<tr>
<td>Audit Logging</td>
<td>Database logging</td>
<td>Complete action tracking</td>
</tr>
<tr>
<td>JWT Authentication</td>
<td>Flask session management</td>
<td>Secure token-based auth</td>
</tr>
<tr>
<td>Fraud Detection</td>
<td>ML-powered scoring</td>
<td>Proactive security monitoring</td>
</tr>
</tbody>
</table>

## 🌍 Tunisia Localization Features

<table>
<thead>
<tr>
<th>Feature</th>
<th>Localization</th>
<th>Benefit</th>
</tr>
</thead>
<tbody>
<tr>
<td>Career Paths</td>
<td>Tunisia-specific job market</td>
<td>Relevant career opportunities</td>
</tr>
<tr>
<td>Educational Recommendations</td>
<td>Local universities and centers</td>
<td>Accessible education options</td>
</tr>
<tr>
<td>Industry Focus</td>
<td>Tunisia economic sectors</td>
<td>Regional industry alignment</td>
</tr>
<tr>
<td>Salary Information</td>
<td>Local market rates</td>
<td>Realistic expectation setting</td>
</tr>
<tr>
<td>Certification Guidance</td>
<td>Local certification bodies</td>
<td>Recognized qualifications</td>
</tr>
</tbody>
</table>

---

**Built with ❤️ for the Tunisian tech community**
