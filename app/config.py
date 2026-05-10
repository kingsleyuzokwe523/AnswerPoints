import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # Fix: Use absolute path for database on PythonAnywhere
    # This will work both locally and on PythonAnywhere
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_PATH, "answerpoint.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # Site settings (defaults)
    SITE_NAME = "AnswerPoint"
    SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')
    
    # WhatsApp and Telegram (defaults, can be overridden in admin)
    DEFAULT_WHATSAPP_LINK = "https://whatsapp.com/channel/yourlink"
    DEFAULT_TELEGRAM_LINK = "https://t.me/yourchannel"
    
    @staticmethod
    def init_directories():
        """Create necessary directories if they don't exist"""
        # Create upload folder
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
            print(f"✅ Created upload folder: {Config.UPLOAD_FOLDER}")
        
        # Create instance folder (for SQLite)
        if not os.path.exists(Config.INSTANCE_PATH):
            os.makedirs(Config.INSTANCE_PATH)
            print(f"✅ Created instance folder: {Config.INSTANCE_PATH}")
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# Different configs for different environments
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-12345')


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'production-secret-key')  # Provide default


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = False


# Select config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}