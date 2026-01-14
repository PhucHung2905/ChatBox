"""
Authentication and authorization module
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from datetime import datetime, timedelta
from database import db, User, AuditLog
from config import JWT_ACCESS_TOKEN_EXPIRES

def generate_token(user_id):
    """Generate JWT token for user"""
    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)
    )
    return access_token


def require_admin(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        claims = get_jwt()
        
        user = User.query.get(identity)
        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Admin access required'
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper


def require_login(fn):
    """Decorator to require user login"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.get(identity)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        # Update last_login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return fn(*args, **kwargs)
    return wrapper


def register_user(email, username, password, full_name=None):
    """Register new user"""
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return {'success': False, 'error': 'Email already registered'}, 400
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return {'success': False, 'error': 'Username already exists'}, 400
    
    try:
        user = User(
            email=email,
            username=username,
            full_name=full_name or username,
            is_admin=False,
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}, 500


def login_user(email, password):
    """Login user"""
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return {'success': False, 'error': 'Email not found'}, 404
    
    if not user.is_active:
        return {'success': False, 'error': 'User account is inactive'}, 403
    
    if not user.check_password(password):
        return {'success': False, 'error': 'Invalid password'}, 401
    
    try:
        # Update last_login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        token = generate_token(user.id)
        
        return {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }, 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500


def get_current_user():
    """Get current authenticated user"""
    try:
        identity = get_jwt_identity()
        user = User.query.get(identity)
        if not user:
            return None
        return user
    except:
        return None


def verify_user_owns_conversation(user_id, conversation_id):
    """Verify that user owns the conversation"""
    from database import ChatHistory
    chat = ChatHistory.query.filter_by(
        user_id=user_id,
        conversation_id=conversation_id
    ).first()
    return chat is not None


def log_admin_action(admin_id, action, target_user_id=None, details=None):
    """Log admin action to audit log"""
    try:
        log = AuditLog(
            admin_id=admin_id,
            action=action,
            target_user_id=target_user_id,
            details=details
        )
        db.session.add(log)
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        print(f"Error logging admin action: {str(e)}")
        return None
