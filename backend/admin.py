"""
Admin management module
"""
from flask import Blueprint, request, jsonify
from auth import require_admin, get_current_user, log_admin_action
from database import db, User, ChatHistory, AuditLog
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Get list of all users"""
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Pagination - SQL Server requires order_by for OFFSET/LIMIT
        users_page = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        users_data = [user.to_dict() for user in users_page.items]
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='view_users_list',
            details=json.dumps({'page': page, 'per_page': per_page})
        )
        
        return jsonify({
            'success': True,
            'users': users_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users_page.total,
                'pages': users_page.pages
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>', methods=['GET'])
@require_admin
def get_user_detail(user_id):
    """Get detailed information about a specific user"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get user's chat statistics
        chat_count = ChatHistory.query.filter_by(user_id=user_id).count()
        first_chat = ChatHistory.query.filter_by(user_id=user_id).order_by(
            ChatHistory.created_at.asc()
        ).first()
        last_chat = ChatHistory.query.filter_by(user_id=user_id).order_by(
            ChatHistory.created_at.desc()
        ).first()
        
        user_dict = user.to_dict()
        user_dict['chat_statistics'] = {
            'total_chats': chat_count,
            'first_chat': first_chat.created_at.isoformat() if first_chat else None,
            'last_chat': last_chat.created_at.isoformat() if last_chat else None
        }
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='view_user_detail',
            target_user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'user': user_dict
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>/chat-history', methods=['GET'])
@require_admin
def get_user_chat_history(user_id):
    """Get chat history of a specific user"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        days = request.args.get('days', None, type=int)
        
        query = ChatHistory.query.filter_by(user_id=user_id)
        
        # Filter by days if specified
        if days:
            start_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(ChatHistory.created_at >= start_date)
        
        # Order by creation date descending
        query = query.order_by(ChatHistory.created_at.desc())
        
        # Pagination
        history_page = query.paginate(page=page, per_page=per_page, error_out=False)
        
        history_data = [chat.to_dict() for chat in history_page.items]
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='view_user_chat_history',
            target_user_id=user_id,
            details=json.dumps({'page': page, 'days': days})
        )
        
        return jsonify({
            'success': True,
            'chat_history': history_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': history_page.total,
                'pages': history_page.pages
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>/promote', methods=['POST'])
@require_admin
def promote_user_to_admin(user_id):
    """Promote a user to admin"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if user.id == current_user.id:
            return jsonify({
                'success': False,
                'error': 'Cannot promote yourself'
            }), 400
        
        if user.is_admin:
            return jsonify({
                'success': False,
                'error': 'User is already an admin'
            }), 400
        
        # Promote user
        user.is_admin = True
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='promote_to_admin',
            target_user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'User {user.username} promoted to admin',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>/demote', methods=['POST'])
@require_admin
def demote_user_from_admin(user_id):
    """Demote an admin to regular user"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if user.id == current_user.id:
            return jsonify({
                'success': False,
                'error': 'Cannot demote yourself'
            }), 400
        
        if not user.is_admin:
            return jsonify({
                'success': False,
                'error': 'User is not an admin'
            }), 400
        
        # Demote user
        user.is_admin = False
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='demote_from_admin',
            target_user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'User {user.username} demoted to regular user',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>/deactivate', methods=['POST'])
@require_admin
def deactivate_user(user_id):
    """Deactivate a user account"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if user.id == current_user.id:
            return jsonify({
                'success': False,
                'error': 'Cannot deactivate yourself'
            }), 400
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User is already deactivated'
            }), 400
        
        # Deactivate user
        user.is_active = False
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='deactivate_user',
            target_user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'User {user.username} deactivated',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/users/<user_id>/activate', methods=['POST'])
@require_admin
def activate_user(user_id):
    """Activate a user account"""
    try:
        current_user = get_current_user()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if user.is_active:
            return jsonify({
                'success': False,
                'error': 'User is already active'
            }), 400
        
        # Activate user
        user.is_active = True
        db.session.commit()
        
        # Log admin action
        log_admin_action(
            admin_id=current_user.id,
            action='activate_user',
            target_user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'User {user.username} activated',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/audit-logs', methods=['GET'])
@require_admin
def get_audit_logs():
    """Get audit logs of admin activities"""
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        days = request.args.get('days', 30, type=int)
        admin_id = request.args.get('admin_id', None)
        
        query = AuditLog.query
        
        # Filter by date range
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(AuditLog.created_at >= start_date)
        
        # Filter by admin_id if specified
        if admin_id:
            query = query.filter_by(admin_id=admin_id)
        
        # Order by creation date descending
        query = query.order_by(AuditLog.created_at.desc())
        
        # Pagination
        logs_page = query.paginate(page=page, per_page=per_page, error_out=False)
        
        logs_data = [log.to_dict() for log in logs_page.items]
        
        return jsonify({
            'success': True,
            'audit_logs': logs_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': logs_page.total,
                'pages': logs_page.pages
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/stats', methods=['GET'])
@require_admin
def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        current_user = get_current_user()
        
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        total_chats = ChatHistory.query.count()
        
        # Get active users in last 24 hours
        last_24h = datetime.utcnow() - timedelta(hours=24)
        active_last_24h = User.query.filter(User.last_login >= last_24h).count()
        
        # Get recent chats
        recent_chats = ChatHistory.query.order_by(
            ChatHistory.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'admin_users': admin_users,
                'regular_users': total_users - admin_users,
                'total_chats': total_chats,
                'active_users_last_24h': active_last_24h
            },
            'recent_chats': [chat.to_dict() for chat in recent_chats]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
