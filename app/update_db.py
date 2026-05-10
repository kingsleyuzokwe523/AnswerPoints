from app import create_app, db
from app.models import Subject, HomeContent, SiteSettings, Admin, Pin, Image, ExamTimetable

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Tables created/updated successfully!")
    
    # Add default home content if missing
    default_sections = [
        ('hero_title', 'AnswerPoint 2026', 'text'),
        ('hero_text', 'Your reliable source for correct WAEC, NECO, and JAMB answers', 'text'),
        ('moving_tagline', '🔥 100% VERIFIED WAEC & NECO ANSWERS — JOIN OUR FREE WHATSAPP & TELEGRAM CHANNELS! 🔥', 'text'),
        ('announcement', '2026 WAEC/NECO Examinations are underway!', 'text'),
        ('instructions', 'Enter your 3-digit PIN to get verified answers', 'text'),
        ('hot_updates_text', '2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE', 'text'),
        ('whatsapp_link', 'https://whatsapp.com/channel/yourlink', 'text'),
        ('telegram_link', 'https://t.me/yourchannel', 'text'),
        ('vip_text', 'Want early VIP answers before the exam?', 'text'),
        ('vip_number', '08065582389', 'text'),
        ('need_help_text', 'Need Help or Updates? → Join Our Official WhatsApp & Telegram Channels Today!', 'text'),
        ('footer_text', '© 2026 AnswerPoint - Your Exam Success Partner', 'text')
    ]
    
    for section, content, content_type in default_sections:
        existing = HomeContent.query.filter_by(section=section).first()
        if not existing:
            new_content = HomeContent(section=section, content=content, content_type=content_type)
            db.session.add(new_content)
    
    # Add default site settings if missing
    default_settings = [
        ('site_name', 'AnswerPoint'),
        ('admin_email', 'support@answerpoint.com'),
        ('primary_color', '#1e40af'),
        ('secondary_color', '#dc2626')
    ]
    
    for key, value in default_settings:
        existing = SiteSettings.query.filter_by(setting_key=key).first()
        if not existing:
            new_setting = SiteSettings(setting_key=key, setting_value=value)
            db.session.add(new_setting)
    
    db.session.commit()
    print("✅ Default content added!")
    
    print("=" * 50)
    print("Database update complete!")
    print("=" * 50)