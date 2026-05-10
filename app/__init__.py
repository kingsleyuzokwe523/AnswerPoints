from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    # Load config
    from config import config_by_name, Config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize directories
    Config.init_directories()
    
    db.init_app(app)
    
    # Import models after db initialization
    from app import models
    
    with app.app_context():
        db.create_all()
        from app.database import init_default_data
        init_default_data()
    
    from app.routes import main_bp
    from app.admin_routes import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app