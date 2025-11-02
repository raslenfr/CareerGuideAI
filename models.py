"""
Database models for the Career Guidance application.

Models:
- User: User accounts with authentication
- ChatHistory: Chat conversation history
- SavedCourse: User's saved course recommendations
"""

from extensions import db
from datetime import datetime


class User(db.Model):
    """User model for authentication and profile management (Enhanced with Wissal features)."""
    __tablename__ = 'users'
    __table_args__ = (
        db.UniqueConstraint('email', 'role', name='uq_email_role'),
    )
    
    # EXISTING FIELDS (preserved)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)  # Removed unique=True, using composite constraint
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # NEW FIELDS from Wissal (enhanced user management)
    username = db.Column(db.String(80), unique=True, nullable=True, index=True)
    full_name = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin/student (teacher removed)
    permissions = db.Column(db.String(500), nullable=True)  # Comma-separated permissions
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    
    # FRAUD DETECTION FIELDS (ML-powered risk scoring)
    risk_score = db.Column(db.Float, nullable=True, index=True)  # 0.0-1.0 fraud probability
    is_suspicious = db.Column(db.Boolean, default=False, index=True)  # Flagged for review
    fraud_reason = db.Column(db.String(255), nullable=True)  # auto-review-required, auto-block-recommended, etc.
    fraud_checked_at = db.Column(db.DateTime, nullable=True)  # When fraud check was performed
    fraud_reviewed_by = db.Column(db.Integer, nullable=True)  # Admin ID who reviewed
    fraud_review_note = db.Column(db.String(500), nullable=True)  # Admin's review notes
    
    # EXISTING RELATIONSHIPS (preserved)
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_courses = db.relationship('SavedCourse', backref='user', lazy=True, cascade='all, delete-orphan')
    career_suggestions = db.relationship('CareerSuggestion', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self, include_fraud=False):
        """Convert user object to dictionary (exclude password)."""
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'full_name': self.full_name or self.name,
            'role': self.role,
            'permissions': self.permissions.split(',') if self.permissions else [],
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Include fraud fields if requested (for admin views)
        if include_fraud:
            data.update({
                'risk_score': self.risk_score,
                'is_suspicious': self.is_suspicious,
                'fraud_reason': self.fraud_reason,
                'fraud_checked_at': self.fraud_checked_at.isoformat() if self.fraud_checked_at else None,
                'fraud_reviewed_by': self.fraud_reviewed_by,
                'fraud_review_note': self.fraud_review_note
            })
        
        return data


class ChatHistory(db.Model):
    """Chat history model to store user conversations."""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    conversation_id = db.Column(db.String(36), nullable=False, index=True)  # UUID for grouping messages
    chat_title = db.Column(db.String(255), nullable=True)  # Title of conversation
    message = db.Column(db.Text, nullable=False)
    reply = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatHistory {self.id} - User {self.user_id} - Conv {self.conversation_id}>'
    
    def to_dict(self):
        """Convert chat history object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'chat_title': self.chat_title,
            'message': self.message,
            'reply': self.reply,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavedCourse(db.Model):
    """Saved course model to store user's bookmarked courses."""
    __tablename__ = 'saved_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_title = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SavedCourse {self.course_title} - User {self.user_id}>'
    
    def to_dict(self):
        """Convert saved course object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_title': self.course_title,
            'provider': self.provider,
            'description': self.description,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CareerSuggestion(db.Model):
    """Career suggestion session model to store user's career path questionnaire results."""
    __tablename__ = 'career_suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False, index=True)  # UUID for session
    session_title = db.Column(db.String(255), nullable=True)  # Title of suggestion session
    answers = db.Column(db.Text, nullable=False)  # JSON string of Q&A pairs
    suggestions = db.Column(db.Text, nullable=False)  # JSON string of career suggestions
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CareerSuggestion {self.id} - User {self.user_id} - Session {self.session_id}>'
    
    def to_dict(self):
        """Convert career suggestion object to dictionary."""
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'session_title': self.session_title,
            'answers': json.loads(self.answers) if self.answers else {},
            'suggestions': json.loads(self.suggestions) if self.suggestions else {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AdminLog(db.Model):
    """Admin action audit log (NEW from Wissal - tracks all admin actions for compliance)."""
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g., "delete_user", "verify_user"
    target_user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)
    
    admin = db.relationship('User', foreign_keys=[admin_id])
    
    def __repr__(self):
        return f'<AdminLog {self.id} - Admin {self.admin_id} - {self.action}>'
    
    def to_dict(self):
        """Convert admin log object to dictionary."""
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action': self.action,
            'target_user_id': self.target_user_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'details': self.details
        }

