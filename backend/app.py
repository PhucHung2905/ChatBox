from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
import os
import traceback
from datetime import datetime
import json

from vector_db import VectorDatabase
from knowledge_base import KnowledgeBaseManager
from llm_handler import LLMHandler
from config import *
from database import db, User, ChatHistory, init_db, create_admin_if_not_exists
from auth import register_user, login_user, require_login, get_current_user
from admin import admin_bp

try:
    from security_config import setup_cors_production, add_security_headers
except ImportError:
    setup_cors_production = None
    add_security_headers = None

# Setup path to frontend folder
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

app = Flask(__name__, static_folder=frontend_path, static_url_path='')

# Configure CORS based on environment
if FLASK_ENV == 'production' and setup_cors_production:
    setup_cors_production(app)
    add_security_headers(app)
else:
    CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Initialize database
db.init_app(app)
jwt = JWTManager(app)

# Initialize components
vector_db = VectorDatabase(EMBEDDINGS_MODEL)
llm = LLMHandler(model=GEMINI_MODEL)

# Global conversation history (will be replaced by database)
conversation_history = {}


# ==================== Health & System ====================

@app.route('/')
def serve_index():
    """Serve the frontend index.html"""
    return send_from_directory(frontend_path, 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


# ==================== Authentication Endpoints ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not email or not username or not password:
            return jsonify({
                'success': False,
                'error': 'Email, username, and password are required'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters'
            }), 400
        
        result, status_code = register_user(email, username, password, full_name)
        return jsonify(result), status_code
    
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        result, status_code = login_user(email, password)
        return jsonify(result), status_code
    
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Get current user information"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify JWT token"""
    try:
        identity = get_jwt_identity()
        user = User.query.get(identity)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'is_admin': user.is_admin
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 401


@app.route('/api/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.json
        
        if 'full_name' in data:
            user.full_name = data['full_name'].strip()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.json
        old_password = data.get('old_password', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not old_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Old and new password are required'
            }), 400
        
        if not user.check_password(old_password):
            return jsonify({
                'success': False,
                'error': 'Old password is incorrect'
            }), 401
        
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 6 characters'
            }), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Knowledge Base ====================

@app.route('/api/init-knowledge-base', methods=['POST'])
def init_knowledge_base():
    """Initialize knowledge base from documents"""
    try:
        print("\n📚 Initializing knowledge base...")
        
        # Load documents from datasets folder
        documents = KnowledgeBaseManager.load_documents(DOCUMENTS_PATH)
        
        if not documents:
            return jsonify({
                'success': False,
                'message': 'No documents found in datasets folder'
            }), 400
        
        # Add to vector database
        vector_db.add_documents(documents)
        
        # Save vector database
        os.makedirs(KB_PATH, exist_ok=True)
        vector_db.save(KB_PATH)
        
        return jsonify({
            'success': True,
            'message': f'Knowledge base initialized with {len(documents)} document chunks',
            'documents_count': len(documents)
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/load-knowledge-base', methods=['POST'])
def load_knowledge_base():
    """Load existing knowledge base from disk"""
    try:
        if os.path.exists(KB_PATH):
            vector_db.load(KB_PATH)
            return jsonify({
                'success': True,
                'message': 'Knowledge base loaded successfully',
                'documents_count': len(vector_db.documents)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Knowledge base not found. Please initialize first.'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/knowledge-base-info', methods=['GET'])
def get_kb_info():
    """Get information about the knowledge base"""
    return jsonify({
        'documents_count': len(vector_db.documents),
        'has_index': vector_db.index is not None,
        'embeddings_model': EMBEDDINGS_MODEL,
        'llm_model': GEMINI_MODEL
    })


# ==================== Chat Endpoints ====================

@app.route('/api/chat', methods=['POST'])
@require_login
def chat():
    """Main chat endpoint - requires authentication"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.json
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', user.id)  # Default to user_id
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize conversation history if needed
        if conversation_id not in conversation_history:
            conversation_history[conversation_id] = []
        
        # Add user message to history
        conversation_history[conversation_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Search knowledge base
        relevant_docs = vector_db.search(user_message, k=5)
        
        # Get response from LLM with context
        response = llm.generate_response(
            user_message=user_message,
            context_docs=relevant_docs,
            conversation_history=conversation_history[conversation_id]
        )
        
        # Add assistant response to history
        conversation_history[conversation_id].append({
            'role': 'assistant',
            'content': response
        })
        
        # Save to database
        chat_record = ChatHistory(
            user_id=user.id,
            conversation_id=conversation_id,
            message=user_message,
            response=response,
            context_used=len(relevant_docs),
            sources=json.dumps([doc.get('metadata', {}) for doc in relevant_docs])
        )
        db.session.add(chat_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response,
            'context_used': len(relevant_docs),
            'sources': [doc.get('metadata', {}) for doc in relevant_docs]
        })
    
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
@require_login
def search():
    """Search the knowledge base"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        k = data.get('k', 5)
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        results = vector_db.search(query, k=k)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat-history', methods=['GET'])
@jwt_required()
def get_user_chat_history():
    """Get user's own chat history"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        conversation_id = request.args.get('conversation_id', None)
        
        query = ChatHistory.query.filter_by(user_id=user.id)
        
        if conversation_id:
            query = query.filter_by(conversation_id=conversation_id)
        
        # Order by creation date descending
        query = query.order_by(ChatHistory.created_at.desc())
        
        # Pagination
        history_page = query.paginate(page=page, per_page=per_page, error_out=False)
        
        history_data = [chat.to_dict() for chat in history_page.items]
        
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


@app.route('/api/clear-conversation', methods=['POST'])
@jwt_required()
def clear_conversation():
    """Clear conversation history"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.json
        conversation_id = data.get('conversation_id', user.id)
        
        if conversation_id in conversation_history:
            del conversation_history[conversation_id]
        
        # Optionally delete from database
        # ChatHistory.query.filter_by(user_id=user.id, conversation_id=conversation_id).delete()
        # db.session.commit()
        
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Admin Routes ====================

app.register_blueprint(admin_bp)


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize database and create admin user
    with app.app_context():
        init_db(app)
        create_admin_if_not_exists(app)
    
    # Try to load existing knowledge base on startup
    if os.path.exists(KB_PATH):
        try:
            vector_db.load(KB_PATH)
            print(f"✓ Loaded knowledge base with {len(vector_db.documents)} documents")
        except Exception as e:
            print(f"⚠ Could not load existing knowledge base: {str(e)}")
    
    print(f"\n🚀 Starting Real Estate ChatBox Backend (v2.0)")
    print(f"✓ Database: SQL Server ({DB_SERVER}/{DB_NAME})")
    print(f"✓ Authentication: JWT Enabled")
    print(f"✓ Admin Panel: Enabled")
    print(f"Server running on http://localhost:{PORT}")
    print(f"API Documentation: http://localhost:{PORT}/docs\n")
    
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
