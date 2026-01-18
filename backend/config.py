import os
from dotenv import load_dotenv

load_dotenv()

# Flask Config
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Gemini Config
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

# Vector Database
VECTOR_DB_PATH = './data/vector_db'
EMBEDDINGS_MODEL = 'all-MiniLM-L6-v2'  # Lightweight embedding model

# Knowledge Base
KB_PATH = './data/knowledge_base'
DOCUMENTS_PATH = './datasets'

# Chat Config
MAX_CONTEXT_LENGTH = 4000
TEMPERATURE = 0.7

# SQL Server Database Config
DB_SERVER = os.getenv('DB_SERVER', 'PHUCHUNG\\SQLEXPRESS')
DB_NAME = os.getenv('DB_NAME', 'ChatBoxDB')
DB_USER = os.getenv('DB_USER', 'PhucHung')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
DB_DRIVER = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
DB_TRUSTED_CONNECTION = os.getenv('DB_TRUSTED_CONNECTION', 'False').lower() == 'true'

# Build SQL Server connection string
if DB_TRUSTED_CONNECTION:
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&charset=utf8'
else:
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Config
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 hours

# Admin Config
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@chatbox.local')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
