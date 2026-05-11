from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    # Get the absolute path to the project root (one level above 'app' folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Tell Flask to look for templates at the project root level
    templates_path = os.path.join(project_root, 'templates')
    static_path = os.path.join(project_root, 'static')
    
    app = Flask(__name__,
                template_folder=templates_path,
                static_folder=static_path)
    
    # Get database URL from environment variable (Render) or use SQLite locally
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # For PostgreSQL on Render/Supabase
        # Fix SSL requirement
        if 'postgres' in database_url and '?' not in database_url:
            database_url += '?sslmode=require'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"Using PostgreSQL database")
    else:
        # For local development with SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, '..', 'instance', 'answerpoint.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        print(f"Using SQLite database at {db_path}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    db.init_app(app)
    
    from app.routes import main_bp
    from app.admin_routes import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    with app.app_context():
        db.create_all()
        print("Database tables created/verified")
    
    # Debug print
    print(f"🔍 Templates folder path: {app.template_folder}")
    print(f"🔍 Templates folder exists: {os.path.exists(app.template_folder)}")
    if os.path.exists(app.template_folder):
        print(f"📁 Files in templates: {os.listdir(app.template_folder)}")
    
    return app
