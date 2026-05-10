from app import db
from app.models import Admin, Subject, HomeContent, ExamTimetable, SiteSettings
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_default_data():
    # Check if admin exists
    if Admin.query.count() == 0:
        admin = Admin(
            username='admin',
            password=generate_password_hash('admin123'),
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: username='admin', password='admin123'")
    
    # Add default home content if empty
    if HomeContent.query.count() == 0:
        default_content = [
            # Hero section
            ('hero_title', 'AnswerPoint'),
            ('hero_text', 'Your reliable source for correct WAEC, NECO, and JAMB answers – quick, accurate, and free.'),
            ('moving_tagline', '🔥 100% VERIFIED WAEC & NECO ANSWERS — JOIN OUR FREE WHATSAPP & TELEGRAM CHANNELS! 🔥'),
            
            # Announcements
            ('announcement', '📢 2026 WAEC/NECO Examinations are underway! Get your verified answers here.'),
            ('instructions', 'Enter your 3-digit PIN and click VIEW ANSWER to get your exam answers instantly.'),
            ('hot_updates_text', '2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE FROM ANSWERPOINT'),
            
            # Social links
            ('whatsapp_link', 'https://whatsapp.com/channel/yourlink'),
            ('telegram_link', 'https://t.me/yourchannel'),
            
            # VIP section
            ('vip_text', 'Want early VIP answers before the exam?'),
            ('vip_number', '08065582389'),
            
            # Help section
            ('need_help_text', 'Need Help? We\'re Here for You!'),
            ('footer_text', 'Powered By AnswerPoint')
        ]
        for section, content in default_content:
            home = HomeContent(section=section, content=content, content_type='text')
            db.session.add(home)
        db.session.commit()
        print("✅ Home content added")
    
    # Add default site settings if empty
    if SiteSettings.query.count() == 0:
        default_settings = [
            ('site_name', 'AnswerPoint', 'text'),
            ('admin_email', 'admin@answerpoint.com', 'email'),
            ('primary_color', '#1e3a8a', 'color'),
            ('secondary_color', '#1d4ed8', 'color'),
            ('waec_timetable_text', '', 'text'),
            ('neco_timetable_text', '', 'text'),
        ]
        for key, value, setting_type in default_settings:
            setting = SiteSettings(setting_key=key, setting_value=value, setting_type=setting_type)
            db.session.add(setting)
        db.session.commit()
        print("✅ Site settings added")
    
    # Add all 80 WAEC subjects if empty
    if Subject.query.count() == 0:
        subjects = [
            # WAEC Subjects 1-40 (First column)
            ('Agricultural Science', 'WAEC', True, 'fa-flask', 1),
            ('Air-conditioning & Refrigeration', 'WAEC', False, 'fa-book', 2),
            ('Animal Husbandry (Alt B)', 'WAEC', True, 'fa-flask', 3),
            ('Applied Electricity', 'WAEC', False, 'fa-book', 4),
            ('Arabic', 'WAEC', False, 'fa-language', 5),
            ('Auto Body Repairs & Spray Painting', 'WAEC', False, 'fa-book', 6),
            ('Auto Electrical Works', 'WAEC', False, 'fa-book', 7),
            ('Auto Mechanical Work', 'WAEC', False, 'fa-book', 8),
            ('Auto Mechanics', 'WAEC', False, 'fa-book', 9),
            ('Automobile Parts Merchandising', 'WAEC', False, 'fa-book', 10),
            ('Basic Electricity', 'WAEC', False, 'fa-book', 11),
            ('Basic Electronics', 'WAEC', False, 'fa-book', 12),
            ('Biology', 'WAEC', True, 'fa-flask', 13),
            ('Block Laying, Bricklaying & Concrete Works', 'WAEC', False, 'fa-book', 14),
            ('Bookkeeping', 'WAEC', False, 'fa-book', 15),
            ('Building Construction', 'WAEC', False, 'fa-book', 16),
            ('Business Management', 'WAEC', False, 'fa-book', 17),
            ('Carpentry & Joinery', 'WAEC', False, 'fa-book', 18),
            ('Catering Craft Practice', 'WAEC', False, 'fa-book', 19),
            ('Chemistry', 'WAEC', True, 'fa-flask', 20),
            ('Christian Religious Studies', 'WAEC', False, 'fa-book', 21),
            ('Civic Education', 'WAEC', False, 'fa-book', 22),
            ('Clothing & Textiles', 'WAEC', False, 'fa-book', 23),
            ('Commerce', 'WAEC', False, 'fa-book', 24),
            ('Computer Studies', 'WAEC', False, 'fa-laptop-code', 25),
            ('Cosmetology', 'WAEC', False, 'fa-book', 26),
            ('Data Processing', 'WAEC', False, 'fa-book', 27),
            ('Dyeing & Bleaching', 'WAEC', False, 'fa-book', 28),
            ('Economics', 'WAEC', False, 'fa-chart-line', 29),
            ('Efik', 'WAEC', False, 'fa-language', 30),
            ('Electrical Installation & Maintenance', 'WAEC', False, 'fa-book', 31),
            ('Electronics', 'WAEC', False, 'fa-book', 32),
            ('English Language', 'WAEC', False, 'fa-book', 33),
            ('Edo', 'WAEC', False, 'fa-language', 34),
            ('Financial Accounting', 'WAEC', False, 'fa-book', 35),
            ('Fisheries (Alt B)', 'WAEC', True, 'fa-flask', 36),
            ('Foods and Nutrition', 'WAEC', True, 'fa-flask', 37),
            ('French', 'WAEC', False, 'fa-language', 38),
            ('Furniture Making', 'WAEC', False, 'fa-book', 39),
            ('Further Mathematics / Mathematics (Elective)', 'WAEC', False, 'fa-calculator', 40),
            
            # WAEC Subjects 41-80 (Second column)
            ('Garment Making', 'WAEC', False, 'fa-book', 41),
            ('General Mathematics / Mathematics (Core)', 'WAEC', False, 'fa-calculator', 42),
            ('Geography', 'WAEC', True, 'fa-flask', 43),
            ('Government', 'WAEC', False, 'fa-book', 44),
            ('GSM Phone Maintenance & Repair', 'WAEC', False, 'fa-book', 45),
            ('Hausa', 'WAEC', False, 'fa-language', 46),
            ('Health Education / Health Science', 'WAEC', False, 'fa-book', 47),
            ('History', 'WAEC', False, 'fa-book', 48),
            ('Home Management', 'WAEC', False, 'fa-book', 49),
            ('Ibibio', 'WAEC', False, 'fa-language', 50),
            ('Igbo', 'WAEC', False, 'fa-language', 51),
            ('Insurance', 'WAEC', False, 'fa-book', 52),
            ('Islamic Studies', 'WAEC', False, 'fa-book', 53),
            ('Leather Goods Manufacturing & Repairs', 'WAEC', False, 'fa-book', 54),
            ('Literature-in-English', 'WAEC', False, 'fa-book', 55),
            ('Machine Woodworking', 'WAEC', False, 'fa-book', 56),
            ('Marketing', 'WAEC', False, 'fa-book', 57),
            ('Metalwork', 'WAEC', False, 'fa-book', 58),
            ('Mining', 'WAEC', False, 'fa-book', 59),
            ('Music', 'WAEC', False, 'fa-music', 60),
            ('Office Practice', 'WAEC', False, 'fa-book', 61),
            ('Painting & Decorating', 'WAEC', False, 'fa-paintbrush', 62),
            ('Photography', 'WAEC', False, 'fa-book', 63),
            ('Physical Education', 'WAEC', False, 'fa-book', 64),
            ('Physics', 'WAEC', True, 'fa-flask', 65),
            ('Plumbing & Pipe Fitting', 'WAEC', False, 'fa-book', 66),
            ('Principles of Cost Accounting', 'WAEC', False, 'fa-book', 67),
            ('Printing Craft Practice', 'WAEC', False, 'fa-book', 68),
            ('Radio, Television & Electronic Works', 'WAEC', False, 'fa-book', 69),
            ('Salesmanship', 'WAEC', False, 'fa-book', 70),
            ('Stenography', 'WAEC', False, 'fa-book', 71),
            ('Store Keeping', 'WAEC', False, 'fa-book', 72),
            ('Store Management', 'WAEC', False, 'fa-book', 73),
            ('Technical Drawing', 'WAEC', False, 'fa-book', 74),
            ('Tourism', 'WAEC', False, 'fa-book', 75),
            ('Upholstery', 'WAEC', False, 'fa-book', 76),
            ('Visual Art', 'WAEC', False, 'fa-paintbrush', 77),
            ('Welding & Fabrication Engineering Craft', 'WAEC', False, 'fa-book', 78),
            ('Woodwork', 'WAEC', False, 'fa-book', 79),
            ('Yoruba', 'WAEC', False, 'fa-language', 80),
        ]
        
        for name, exam_type, practical, icon, order in subjects:
            subject = Subject(
                name=name, 
                exam_type=exam_type, 
                has_practical=practical,
                icon=icon,
                display_order=order,
                show_on_homepage=True
            )
            db.session.add(subject)
        db.session.commit()
        print(f"✅ {len(subjects)} subjects added")
    
    print("\n🎉 Database initialization complete!")
    print("=" * 40)
    print("Login Credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("=" * 40)