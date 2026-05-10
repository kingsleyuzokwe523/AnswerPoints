from app import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    exam_type = db.Column(db.String(10), nullable=False)
    has_practical = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50), default='fa-book')
    show_on_homepage = db.Column(db.Boolean, default=True)

class Pin(db.Model):
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    pin_code = db.Column(db.String(3), unique=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=True)  # nullable=True is correct
    subject_name = db.Column(db.String(200), nullable=True)
    main_title = db.Column(db.String(500), default='OFFICIAL ANSWERS')
    posted_by = db.Column(db.String(200), default='AnswerPoint')
    header_color = db.Column(db.String(7), default='#ffffff')
    answer_text_color = db.Column(db.String(7), default='#1f2937')
    answer_text = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    # NO created_at column here!

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id', ondelete='CASCADE'), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # REMOVE this line if it exists:
    # file_name = db.Column(db.String(200))

    pin = db.relationship('Pin', backref=db.backref('images', lazy=True, cascade='all, delete-orphan'))

class HomeContent(db.Model):
    __tablename__ = 'home_content'
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_type = db.Column(db.String(50), default='text')

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=True)
    setting_type = db.Column(db.String(50), default='text')

class ExamTimetable(db.Model):
    __tablename__ = 'exam_timetables'
    id = db.Column(db.Integer, primary_key=True)
    exam_type = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    paper = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, default=2026)

# Alias for backward compatibility
Timetable = ExamTimetable
# ==================== ALIAS FOR BACKWARD COMPATIBILITY ====================
# This allows your routes to use 'Timetable' instead of 'ExamTimetable'
Timetable = ExamTimetable


# ==================== HELPER FUNCTIONS ====================

def init_home_content():
    """Initialize default home content if not exists"""
    default_sections = [
        ('hero_title', 'AnswerPoint', 'text'),
        ('hero_text', 'Your reliable source for correct WAEC, NECO, and JAMB answers – quick, accurate, and free.', 'text'),
        ('moving_tagline', '🔥 100% VERIFIED WAEC & NECO ANSWERS — JOIN OUR FREE WHATSAPP & TELEGRAM CHANNELS! 🔥', 'text'),
        ('announcement', '', 'text'),
        ('instructions', '', 'text'),
        ('whatsapp_link', '#', 'link'),
        ('telegram_link', '#', 'link'),
        ('footer_text', 'Powered By AnswerPoint', 'text'),
        ('vip_text', 'Want early VIP answers before the exam?', 'text'),
        ('vip_number', '08065582389', 'text'),
        ('need_help_text', 'Need Help? We\'re Here for You!', 'text'),
        ('hot_updates_text', '2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE', 'text'),
        ('support_email', 'support@answerpoint.com', 'email'),

        # ========== DESIGN SETTINGS (ADD THESE) ==========
        ('primary_green', '#28a745', 'color'),
        ('primary_red', '#ff0000', 'color'),
        ('primary_black', '#000000', 'color'),
        ('button_radius', '30px', 'text'),
        ('card_radius', '12px', 'text'),
        ('font_family', 'Inter, Arial, sans-serif', 'text'),
        ('loading_bar_color', '#28a745', 'color'),
        ('footer_bg', '#000000', 'color'),
        ('footer_text_color', '#ffffff', 'color'),
        ('footer_link_color', '#ffcc00', 'color'),
    ]

    for section, content, content_type in default_sections:
        if not HomeContent.query.filter_by(section=section).first():
            home = HomeContent(section=section, content=content, content_type=content_type)
            db.session.add(home)

    db.session.commit()


def init_site_settings():
    """Initialize default site settings if not exists"""
    default_settings = [
        ('site_name', 'AnswerPoint', 'text'),
        ('primary_color', '#1e3a8a', 'color'),
        ('secondary_color', '#1d4ed8', 'color'),
        ('waec_timetable_text', '', 'text'),
        ('neco_timetable_text', '', 'text'),
    ]

    for key, value, setting_type in default_settings:
        if not SiteSettings.query.filter_by(setting_key=key).first():
            setting = SiteSettings(setting_key=key, setting_value=value, setting_type=setting_type)
            db.session.add(setting)

    db.session.commit()


def init_db():
    """Initialize database with default data"""
    db.create_all()
    init_home_content()
    init_site_settings()