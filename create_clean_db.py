import os
import sys

# Delete database if exists
db_path = 'instance/answerpoint.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old database deleted")

# Now create fresh database
from app import create_app, db
from app.models import Admin, Subject, HomeContent, ExamTimetable
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Tables created")
    
    # Create admin
    admin = Admin(
        username='admin',
        password=generate_password_hash('admin123'),
        created_at=datetime.utcnow()
    )
    db.session.add(admin)
    
    # Add home content
    home_data = [
        ('hero_title', 'AnswerPoint 2026'),
        ('hero_text', 'Your reliable source for WAEC & NECO exam answers.'),
        ('announcement', '📢 2026 WAEC/NECO Examinations are underway!'),
        ('instructions', 'Enter your 3-digit PIN to get verified answers.'),
        ('whatsapp_link', 'https://whatsapp.com/channel/yourlink'),
        ('telegram_link', 'https://t.me/yourchannel'),
        ('footer_text', '© 2026 AnswerPoint - Your Exam Success Partner')
    ]
    
    for section, content in home_data:
        home = HomeContent(section=section, content=content)
        db.session.add(home)
    
    # Add sample subjects
    subjects = [
        ('Mathematics', 'WAEC', 0),
        ('English Language', 'WAEC', 0),
        ('Physics', 'WAEC', 1),
        ('Chemistry', 'WAEC', 1),
        ('Biology', 'WAEC', 1),
    ]
    
    for name, exam_type, practical in subjects:
        subject = Subject(name=name, exam_type=exam_type, has_practical=practical)
        db.session.add(subject)
    
    db.session.commit()
    
    print("=" * 50)
    print("DATABASE CREATED SUCCESSFULLY!")
    print("Admin: admin / admin123")
    print("=" * 50)