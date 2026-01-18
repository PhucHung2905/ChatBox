"""
Database models and initialization for SQL Server
"""
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(500), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    chat_histories = db.relationship('ChatHistory', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_password=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        if include_password:
            data['password_hash'] = self.password_hash
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'


class ChatHistory(db.Model):
    """Chat history model for storing conversations"""
    __tablename__ = 'chat_histories'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    conversation_id = db.Column(db.String(255), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    context_used = db.Column(db.Integer, default=0)
    sources = db.Column(db.Text, nullable=True)  # JSON stored as text
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='chat_histories')
    
    def to_dict(self):
        """Convert chat history to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'message': self.message,
            'response': self.response,
            'context_used': self.context_used,
            'sources': self.sources,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<ChatHistory {self.id}>'


class UserInfoRequest(db.Model):
    """User information request before chat - for admin review"""
    __tablename__ = 'user_info_requests'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(255), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)
    is_reviewed = db.Column(db.Boolean, default=False, index=True)
    reviewed_by = db.Column(db.String(36), nullable=True)  # Admin ID
    notes = db.Column(db.Text, nullable=True)  # Admin notes
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'message': self.message,
            'is_reviewed': self.is_reviewed,
            'reviewed_by': self.reviewed_by,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<UserInfoRequest {self.full_name}>'


class AuditLog(db.Model):
    """Audit log for admin activities"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_id = db.Column(db.String(36), nullable=False, index=True)
    action = db.Column(db.String(255), nullable=False)
    target_user_id = db.Column(db.String(36), nullable=True, index=True)
    details = db.Column(db.Text, nullable=True)  # JSON stored as text
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action': self.action,
            'target_user_id': self.target_user_id,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'


def init_db(app):
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully")


def create_admin_if_not_exists(app):
    """Create default admin user if not exists"""
    from config import ADMIN_EMAIL, ADMIN_PASSWORD
    
    with app.app_context():
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=ADMIN_EMAIL,
                username='admin',
                full_name='Administrator',
                is_admin=True,
                is_active=True
            )
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print(f"✓ Admin user created: {ADMIN_EMAIL}")
        else:
            print(f"✓ Admin user already exists: {ADMIN_EMAIL}")


def add_audit_log(admin_id, action, target_user_id=None, details=None):
    """Add audit log entry"""
    log = AuditLog(
        admin_id=admin_id,
        action=action,
        target_user_id=target_user_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()
    return log
