# 🧩 BACKEND INTEGRATION PLAN
## Career Suggested Backend + Wissal Backend Merger

---

## 📊 COMPLETE PROJECT COMPARISON

### **Current Career Suggested Backend (This Project)**

#### **🏗️ Architecture**
- **Framework:** Flask (Python)
- **Port:** 5000
- **Database:** SQLite (`instance/course_recommendation.db`)
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Bcrypt (simple password hashing, no JWT)
- **LLM Service:** Groq API (llama-3.3-70b-versatile)

#### **📂 Project Structure**
```
careersuggestion_Backend/
├── app.py                      # Main Flask application
├── extensions.py               # DB and Bcrypt initialization
├── models.py                   # Database models (4 tables)
├── blueprints/
│   ├── auth_bp.py             # Basic auth (signup/login)
│   ├── chatbot_bp.py          # AI career chatbot
│   ├── suggester_bp.py        # Career suggestion questionnaire
│   ├── recommender_bp.py      # Course recommender
│   ├── test_recording_bp.py   # Testing framework
│   └── test_reports_bp.py     # Test reporting
├── services/
│   ├── llm_service.py         # Groq LLM integration
│   └── job_search_service.py  # Job search logic
└── tests/                      # Diagnostic testing framework
```

#### **🗄️ Database Models**
1. **User**
   - Fields: `id`, `email`, `password_hash`, `name`, `created_at`
   - No roles, no permissions, no email verification
   - Simple authentication only

2. **ChatHistory**
   - Fields: `id`, `user_id`, `conversation_id`, `chat_title`, `message`, `reply`, `created_at`
   - Stores AI chatbot conversations

3. **SavedCourse**
   - Fields: `id`, `user_id`, `course_title`, `provider`, `description`, `url`, `created_at`
   - Bookmarked courses

4. **CareerSuggestion**
   - Fields: `id`, `user_id`, `session_id`, `session_title`, `answers`, `suggestions`, `created_at`
   - Career path questionnaire results

#### **🔐 Authentication System**
- **Type:** Basic username/password with bcrypt
- **Sessions:** Flask secret key (no JWT)
- **No features:**
  - ❌ No role-based access control (RBAC)
  - ❌ No email verification
  - ❌ No JWT tokens
  - ❌ No password reset
  - ❌ No admin panel
  - ❌ No fraud detection

#### **🎯 Core Features (KEEP THESE)**
✅ **AI Chatbot** - Career guidance conversations  
✅ **Career Suggester** - 11-question career path survey  
✅ **Course Recommender** - Job-based course recommendations  
✅ **Groq LLM Integration** - Intelligent responses  
✅ **Chat History** - Save and retrieve conversations  
✅ **Diagnostic Testing Framework** - AI test system  

#### **📡 API Endpoints (Current)**
```
Authentication:
  POST /api/auth/signup
  POST /api/auth/login

AI Features:
  POST /api/chatbot/message
  GET  /api/chatbot/conversations
  GET  /api/chatbot/conversations/<id>
  DELETE /api/chatbot/conversations/<id>
  POST /api/chatbot/save-conversation

Career Suggester:
  GET  /api/suggester/start
  POST /api/suggester/answer
  POST /api/suggester/save-session
  GET  /api/suggester/sessions
  GET  /api/suggester/sessions/<session_id>
  DELETE /api/suggester/sessions/<session_id>

Course Recommender:
  POST /api/recommender/start
  POST /api/recommender/submit
```

---

### **Wissal Backend (Source for User Management)**

#### **🏗️ Architecture**
- **Framework:** FastAPI (Python)
- **Port:** 8000
- **Database:** SQLite (`test.db`)
- **ORM:** SQLAlchemy (direct, not Flask-SQLAlchemy)
- **Authentication:** JWT (jose) + OAuth2 + Bcrypt
- **AI Feature:** ML-based fraud detection for signups

#### **📂 Project Structure**
```
wissal_backend/
├── main.py                     # FastAPI application
├── auth.py                     # JWT authentication router
├── crud.py                     # Admin CRUD operations
├── models.py                   # User and AdminLog models
├── schemas.py                  # Pydantic validation schemas
├── database.py                 # SQLAlchemy config
├── dependencies.py             # Dependency injection
├── features.py                 # ML feature extraction
├── IA/
│   ├── ml_model.py            # Fraud detection model
│   ├── train_model.py         # Model training
│   ├── predict_signup.py      # Risk prediction
│   └── signup_risk_model.joblib
├── utils/
│   ├── send_email.py          # SMTP email sender
│   ├── email_verification.py  # 6-digit code verification
│   ├── email_welcome.py       # Welcome email template
│   └── email_reset.py         # Password reset email
└── alembic/                    # Database migrations
```

#### **🗄️ Database Models**
1. **User (Enhanced)**
   - Fields: `id`, `username`, `email`, `full_name`, `hashed_password`
   - **Roles:** `admin`, `teacher`, `student`
   - **Permissions:** Comma-separated string (e.g., "view_courses,edit_content")
   - **Email Verification:** `is_verified`, `verification_code`, `verification_sent_at`

2. **AdminLog**
   - Fields: `id`, `admin_id`, `action`, `target_user_id`, `timestamp`, `details`
   - Tracks all admin actions for audit trail

#### **🔐 Authentication System (SUPERIOR)**
- **Type:** JWT tokens (HS256 algorithm)
- **Token Expiry:** 60 minutes
- **OAuth2 compliant:** OAuth2PasswordBearer
- **Features:**
  - ✅ JWT access tokens
  - ✅ Role-based access control (admin/teacher/student)
  - ✅ Granular permissions system
  - ✅ Email verification with 6-digit codes
  - ✅ Password reset via email
  - ✅ Admin action logging
  - ✅ AI-powered fraud detection (ML model)

#### **🤖 AI Fraud Detection**
- **Model:** Logistic Regression with SMOTE balancing
- **Features:** 10 behavioral signals (disposable email, entropy, blacklist, etc.)
- **Output:** Risk score (0.0-1.0) with thresholds:
  - T_REVIEW = 0.4 (manual review)
  - T_BLOCK = 0.8 (auto-block)
- **Endpoint:** `POST /users/risk-ml`

#### **📧 Email System**
- **Provider:** Gmail SMTP (put your email here)
- **Features:**
  - Welcome emails on signup
  - 6-digit verification codes (10-min expiry)
  - Password reset emails
  - Professional HTML templates

#### **📡 API Endpoints (Wissal)**
```
Authentication:
  POST /users/           # Register (with AI fraud check)
  POST /login            # Login (returns JWT)
  GET  /me               # Current user info

Admin Management:
  GET    /users/all      # List all users
  GET    /users/stats    # User statistics
  DELETE /users/{id}     # Delete user
  PUT    /users/{id}     # Update user
  PUT    /users/{id}/verify  # Verify user
  GET    /admin/logs     # Admin action logs

AI/ML:
  POST /users/risk-ml    # Check signup risk score
```

---

## 🔄 INTEGRATION STRATEGY

### **Decision Matrix: What to Keep vs Replace**

| Component | Career Suggested | Wissal | **DECISION** |
|-----------|-----------------|--------|--------------|
| **Framework** | Flask | FastAPI | **KEEP Flask** (easier integration) |
| **User Model** | Basic (name, email, password) | Advanced (roles, permissions, verification) | **USE Wissal** |
| **Authentication** | Basic bcrypt | JWT + OAuth2 + RBAC | **USE Wissal (adapted to Flask)** |
| **AI Chatbot** | ✅ Full system | ❌ None | **KEEP Career Suggested** |
| **Career Suggester** | ✅ Full system | ❌ None | **KEEP Career Suggested** |
| **Course Recommender** | ✅ Full system | ❌ None | **KEEP Career Suggested** |
| **Fraud Detection** | ❌ None | ✅ ML model | **INTEGRATE Wissal** |
| **Email System** | ❌ None | ✅ Full SMTP | **INTEGRATE Wissal** |
| **Admin Panel** | ❌ None | ✅ Full CRUD + logs | **INTEGRATE Wissal** |
| **Database** | SQLite | SQLite | **KEEP Career Suggested DB, migrate schema** |

---

## 🛠️ DETAILED INTEGRATION STEPS

### **Phase 1: Preparation & Backup**
1. ✅ **Backup current database**
   ```bash
   cp instance/course_recommendation.db instance/course_recommendation_backup.db
   ```

2. ✅ **Create migration script**
   - Add new fields to User model
   - Create AdminLog table
   - Preserve existing data

### **Phase 2: Database Schema Migration**

#### **Update User Model (models.py)**
```python
class User(db.Model):
    __tablename__ = 'users'
    
    # Existing fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # NEW FIELDS from Wissal
    username = db.Column(db.String(80), unique=True, nullable=True, index=True)  # Can be same as name initially
    full_name = db.Column(db.String(150), nullable=True)  # Alias for 'name'
    role = db.Column(db.String(20), nullable=False, default='student')  # admin/teacher/student
    permissions = db.Column(db.String(500), nullable=True)  # Comma-separated
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    
    # Existing relationships
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_courses = db.relationship('SavedCourse', backref='user', lazy=True, cascade='all, delete-orphan')
    career_suggestions = db.relationship('CareerSuggestion', backref='user', lazy=True, cascade='all, delete-orphan')
```

#### **Add AdminLog Model (models.py)**
```python
class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)
    
    admin = db.relationship('User', foreign_keys=[admin_id])
```

### **Phase 3: Authentication System Upgrade**

#### **Create JWT utilities (new file: `utils/jwt_helper.py`)**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

#### **Update auth_bp.py (Enhanced Authentication)**
Add these features:
- JWT token generation on login
- Role-based middleware
- Email verification endpoints
- Password reset flow
- Admin-only routes protection

### **Phase 4: Email System Integration**

#### **Copy from Wissal → Career Suggested**
```bash
# Create utils directory
mkdir -p utils

# Copy email utilities from Wissal
cp ../wissal_backend/utils/send_email.py utils/
cp ../wissal_backend/utils/email_verification.py utils/
cp ../wissal_backend/utils/email_welcome.py utils/
cp ../wissal_backend/utils/email_reset.py utils/
```

#### **Update requirements.txt**
```
Flask>=2.0
groq>=0.22.0
python-dotenv>=0.15
requests>=2.25
Flask-CORS>=3.0.10
Flask-SQLAlchemy>=3.0.0
Flask-Bcrypt>=1.0.1

# NEW from Wissal
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
email-validator>=2.0.0
```

### **Phase 5: AI Fraud Detection Integration**

#### **Copy ML system from Wissal**
```bash
# Create IA directory
mkdir -p IA

# Copy entire ML system
cp -r ../wissal_backend/IA/* IA/
```

#### **Add fraud check to signup (blueprints/auth_bp.py)**
```python
from IA.ml_model import predict_risk

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # ... existing validation ...
    
    # NEW: AI fraud detection
    fraud_check_payload = {
        "username": name,
        "email": email,
        "full_name": name,
        "time_to_submit_ms": data.get('time_to_submit', 5000)
    }
    
    try:
        risk_result = predict_risk(fraud_check_payload)
        if risk_result.get('decision') == 'block':
            log.warning(f"Signup blocked by fraud detection: {email}")
            return jsonify({
                "success": False, 
                "error": "Account creation flagged for security review"
            }), 403
    except Exception as e:
        log.error(f"Fraud detection error: {e}")
        # Continue signup even if fraud check fails
    
    # ... rest of signup logic ...
```

### **Phase 6: Admin Panel Integration**

#### **Create new blueprint: blueprints/admin_bp.py**
```python
from flask import Blueprint, request, jsonify
from extensions import db
from models import User, AdminLog
from utils.jwt_helper import decode_token
import logging

log = logging.getLogger(__name__)
admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/admin')

def require_admin(func):
    """Decorator to require admin role"""
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"success": False, "error": "Authentication required"}), 401
        
        payload = decode_token(token)
        if not payload or payload.get('role') != 'admin':
            return jsonify({"success": False, "error": "Admin access required"}), 403
        
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    users = User.query.all()
    return jsonify({
        "success": True,
        "users": [user.to_dict() for user in users]
    })

# ... more admin endpoints ...
```

### **Phase 7: Testing & Validation**

#### **Test Checklist**
- [ ] Existing users can still login
- [ ] New JWT tokens work with all endpoints
- [ ] AI chatbot still functions
- [ ] Career suggester still works
- [ ] Course recommender still works
- [ ] New admin panel accessible
- [ ] Email verification works
- [ ] Fraud detection blocks suspicious signups
- [ ] All existing data preserved

---

## 📊 FINAL UNIFIED ARCHITECTURE

### **Technology Stack**
```yaml
Framework: Flask 2.0+
Database: SQLite (course_recommendation.db)
ORM: Flask-SQLAlchemy
Authentication: JWT (python-jose) + Flask-Bcrypt
LLM: Groq API (llama-3.3-70b-versatile)
ML: scikit-learn (fraud detection)
Email: Gmail SMTP
Testing: Custom diagnostic framework
```

### **Unified API Endpoints (After Integration)**
```
Authentication:
  POST   /api/auth/signup              # With fraud detection
  POST   /api/auth/login               # Returns JWT token
  GET    /api/auth/me                  # Current user info
  POST   /api/auth/verify-email        # Email verification
  POST   /api/auth/forgot-password     # Request reset code
  POST   /api/auth/reset-password      # Reset with code

Admin Panel:
  GET    /api/admin/users              # List all users
  GET    /api/admin/stats              # User statistics
  DELETE /api/admin/users/{id}         # Delete user
  PUT    /api/admin/users/{id}         # Update user
  PUT    /api/admin/users/{id}/verify  # Manually verify
  GET    /api/admin/logs               # Admin action logs

AI Features (Preserved):
  POST   /api/chatbot/message
  GET    /api/chatbot/conversations
  GET    /api/chatbot/conversations/{id}
  DELETE /api/chatbot/conversations/{id}
  POST   /api/chatbot/save-conversation

  GET    /api/suggester/start
  POST   /api/suggester/answer
  POST   /api/suggester/save-session
  GET    /api/suggester/sessions
  GET    /api/suggester/sessions/{id}
  DELETE /api/suggester/sessions/{id}

  POST   /api/recommender/start
  POST   /api/recommender/submit

ML/Security:
  POST   /api/ml/check-signup-risk     # Fraud detection
```

### **Database Schema (Final)**
```
Tables:
  ├── users (enhanced with roles, permissions, verification)
  ├── admin_logs (new - audit trail)
  ├── chat_history (preserved)
  ├── saved_courses (preserved)
  └── career_suggestions (preserved)
```

---

## 🎯 SUCCESS CRITERIA

### **Must Have**
✅ All existing AI features work unchanged  
✅ JWT authentication replaces basic auth  
✅ Role-based access control functional  
✅ Email verification system active  
✅ Fraud detection protects signups  
✅ Admin panel accessible and secure  
✅ All existing user data preserved  

### **Performance Targets**
- API response time: < 2s for LLM calls, < 200ms for CRUD
- Database migrations: < 30 seconds
- Zero downtime during migration (use maintenance mode)

### **Security Enhancements**
- JWT tokens with 60-min expiry
- Bcrypt password hashing (72-char truncation)
- Admin action logging for audit
- ML-based fraud detection (0.8 threshold for blocking)
- Email verification before full access

---

## 🚨 CRITICAL NOTES

### **Breaking Changes**
1. **Login Response Changes:**
   - Old: `{"success": true, "user": {...}}`
   - New: `{"success": true, "access_token": "...", "token_type": "bearer", "user": {...}}`

2. **Protected Endpoints:**
   - All `/api/chatbot/*`, `/api/suggester/*`, `/api/recommender/*` now require JWT in header:
     ```
     Authorization: Bearer <token>
     ```

3. **Frontend Updates Required:**
   - Store JWT token in localStorage/sessionStorage
   - Add Authorization header to all API calls
   - Handle 401/403 errors (token expiry, insufficient permissions)

### **Environment Variables (New)**
```bash
# .env file
FLASK_SECRET_KEY=your-strong-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
GROQ_API_KEY=your-groq-api-key

# Email settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=put your email here
SMTP_PASSWORD=your-app-password
```

### **Migration Rollback Plan**
If integration fails:
1. Restore backup database: `cp instance/course_recommendation_backup.db instance/course_recommendation.db`
2. Revert code changes via git: `git reset --hard <commit-before-integration>`
3. Restart Flask server

---

## 📅 ESTIMATED TIMELINE

- **Phase 1-2 (Database):** 2-3 hours
- **Phase 3 (Auth):** 4-5 hours
- **Phase 4 (Email):** 2 hours
- **Phase 5 (Fraud Detection):** 2 hours
- **Phase 6 (Admin Panel):** 3-4 hours
- **Phase 7 (Testing):** 4-6 hours

**Total:** ~20-25 hours of development + testing

---

## 🎓 FINAL RECOMMENDATIONS

1. **Use Git branches:** Create `feature/wissal-integration` branch
2. **Test incrementally:** Don't integrate everything at once
3. **Update documentation:** Keep README.md current
4. **Frontend coordination:** Ensure frontend team knows about JWT changes
5. **Security audit:** Review all admin endpoints before production
6. **Environment configs:** Use .env for all secrets (never commit!)

---

**Created:** October 28, 2025  
**Status:** Ready for Implementation  
**Next Step:** Begin Phase 1 (Database Backup & Migration Script)

