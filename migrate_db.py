import sqlite3
import os

# First, ensure database and tables exist
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables created/verified")

# Now run the migration
db_path = 'instance/answerpoint.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 50)
print("Starting database migration...")
print("=" * 50)

# 1. Add content_type column to home_content
try:
    cursor.execute("ALTER TABLE home_content ADD COLUMN content_type TEXT DEFAULT 'text'")
    print("✅ Added content_type column to home_content")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ content_type column already exists")
    else:
        print(f"Note: {e}")

# 2. Add icon column to subjects
try:
    cursor.execute("ALTER TABLE subjects ADD COLUMN icon TEXT DEFAULT 'fa-book'")
    print("✅ Added icon column to subjects")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ icon column already exists")

# 3. Add show_on_homepage column to subjects
try:
    cursor.execute("ALTER TABLE subjects ADD COLUMN show_on_homepage BOOLEAN DEFAULT 1")
    print("✅ Added show_on_homepage column to subjects")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ show_on_homepage column already exists")

# 4. Add display_order column to subjects
try:
    cursor.execute("ALTER TABLE subjects ADD COLUMN display_order INTEGER DEFAULT 0")
    print("✅ Added display_order column to subjects")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ display_order column already exists")

# 5. Add text_color column to pins
try:
    cursor.execute("ALTER TABLE pins ADD COLUMN text_color VARCHAR(7) DEFAULT '#000000'")
    print("✅ Added text_color column to pins")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ text_color column already exists")
    else:
        print(f"Note: {e}")

# 6. Add display_order column to images
try:
    cursor.execute("ALTER TABLE images ADD COLUMN display_order INTEGER DEFAULT 0")
    print("✅ Added display_order column to images")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ display_order column already exists")
    else:
        print(f"Note: {e}")

# 7. Add default home content if missing
default_sections = [
    ('hero_title', 'AnswerPoint', 'text'),
    ('hero_text', 'Your reliable source for correct WAEC, NECO, and JAMB answers', 'text'),
    ('moving_tagline', '🔥 100% VERIFIED WAEC & NECO ANSWERS', 'text'),
    ('announcement', '📢 2026 WAEC/NECO Examinations are underway!', 'text'),
    ('instructions', 'Enter your 3-digit PIN to get verified answers', 'text'),
    ('hot_updates_text', '2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE', 'text'),
    ('whatsapp_link', 'https://whatsapp.com/channel/yourlink', 'link'),
    ('telegram_link', 'https://t.me/yourchannel', 'link'),
    ('vip_text', 'Want early VIP answers before the exam?', 'text'),
    ('vip_number', '08065582389', 'text'),
    ('need_help_text', 'Need Help? We\'re Here for You!', 'text'),
    ('footer_text', 'Powered By AnswerPoint', 'text')
]

for section, content, content_type in default_sections:
    try:
        cursor.execute(
            "INSERT INTO home_content (section, content, content_type) VALUES (?, ?, ?)",
            (section, content, content_type)
        )
        print(f"✅ Added home section: {section}")
    except sqlite3.IntegrityError:
        print(f"⏭️ Already exists: {section}")

# 8. Add default site settings
default_settings = [
    ('site_name', 'AnswerPoint', 'text'),
    ('admin_email', 'support@answerpoint.com', 'email'),
    ('primary_color', '#1e40af', 'color'),
    ('secondary_color', '#dc2626', 'color'),
    ('waec_timetable_text', '', 'text'),
    ('neco_timetable_text', '', 'text'),
]

for key, value, setting_type in default_settings:
    try:
        cursor.execute(
            "INSERT INTO site_settings (setting_key, setting_value, setting_type) VALUES (?, ?, ?)",
            (key, value, setting_type)
        )
        print(f"✅ Added setting: {key}")
    except sqlite3.IntegrityError:
        print(f"⏭️ Setting already exists: {key}")

# 9. Check if subjects table has data
cursor.execute("SELECT COUNT(*) FROM subjects")
count = cursor.fetchone()[0]
print(f"\n📊 Current subjects count: {count}")

if count < 80:
    print("\n🔄 Adding 80 WAEC subjects...")
    
    waec_subjects = [
        (1, 'Agricultural Science', 1, 'fa-flask'),
        (2, 'Air-conditioning & Refrigeration', 0, 'fa-book'),
        (3, 'Animal Husbandry (Alt B)', 1, 'fa-flask'),
        (4, 'Applied Electricity', 0, 'fa-book'),
        (5, 'Arabic', 0, 'fa-language'),
        (6, 'Auto Body Repairs & Spray Painting', 0, 'fa-book'),
        (7, 'Auto Electrical Works', 0, 'fa-book'),
        (8, 'Auto Mechanical Work', 0, 'fa-book'),
        (9, 'Auto Mechanics', 0, 'fa-book'),
        (10, 'Automobile Parts Merchandising', 0, 'fa-book'),
        (11, 'Basic Electricity', 0, 'fa-book'),
        (12, 'Basic Electronics', 0, 'fa-book'),
        (13, 'Biology', 1, 'fa-flask'),
        (14, 'Block Laying, Bricklaying & Concrete Works', 0, 'fa-book'),
        (15, 'Bookkeeping', 0, 'fa-book'),
        (16, 'Building Construction', 0, 'fa-book'),
        (17, 'Business Management', 0, 'fa-book'),
        (18, 'Carpentry & Joinery', 0, 'fa-book'),
        (19, 'Catering Craft Practice', 0, 'fa-book'),
        (20, 'Chemistry', 1, 'fa-flask'),
        (21, 'Christian Religious Studies', 0, 'fa-book'),
        (22, 'Civic Education', 0, 'fa-book'),
        (23, 'Clothing & Textiles', 0, 'fa-book'),
        (24, 'Commerce', 0, 'fa-book'),
        (25, 'Computer Studies', 0, 'fa-laptop-code'),
        (26, 'Cosmetology', 0, 'fa-book'),
        (27, 'Data Processing', 0, 'fa-book'),
        (28, 'Dyeing & Bleaching', 0, 'fa-book'),
        (29, 'Economics', 0, 'fa-chart-line'),
        (30, 'Efik', 0, 'fa-language'),
        (31, 'Electrical Installation & Maintenance', 0, 'fa-book'),
        (32, 'Electronics', 0, 'fa-book'),
        (33, 'English Language', 0, 'fa-book'),
        (34, 'Edo', 0, 'fa-language'),
        (35, 'Financial Accounting', 0, 'fa-book'),
        (36, 'Fisheries (Alt B)', 1, 'fa-flask'),
        (37, 'Foods and Nutrition', 1, 'fa-flask'),
        (38, 'French', 0, 'fa-language'),
        (39, 'Furniture Making', 0, 'fa-book'),
        (40, 'Further Mathematics / Mathematics (Elective)', 0, 'fa-calculator'),
        (41, 'Garment Making', 0, 'fa-book'),
        (42, 'General Mathematics / Mathematics (Core)', 0, 'fa-calculator'),
        (43, 'Geography', 1, 'fa-flask'),
        (44, 'Government', 0, 'fa-book'),
        (45, 'GSM Phone Maintenance & Repair', 0, 'fa-book'),
        (46, 'Hausa', 0, 'fa-language'),
        (47, 'Health Education / Health Science', 0, 'fa-book'),
        (48, 'History', 0, 'fa-book'),
        (49, 'Home Management', 0, 'fa-book'),
        (50, 'Ibibio', 0, 'fa-language'),
        (51, 'Igbo', 0, 'fa-language'),
        (52, 'Insurance', 0, 'fa-book'),
        (53, 'Islamic Studies', 0, 'fa-book'),
        (54, 'Leather Goods Manufacturing & Repairs', 0, 'fa-book'),
        (55, 'Literature-in-English', 0, 'fa-book'),
        (56, 'Machine Woodworking', 0, 'fa-book'),
        (57, 'Marketing', 0, 'fa-book'),
        (58, 'Metalwork', 0, 'fa-book'),
        (59, 'Mining', 0, 'fa-book'),
        (60, 'Music', 0, 'fa-music'),
        (61, 'Office Practice', 0, 'fa-book'),
        (62, 'Painting & Decorating', 0, 'fa-paintbrush'),
        (63, 'Photography', 0, 'fa-book'),
        (64, 'Physical Education', 0, 'fa-book'),
        (65, 'Physics', 1, 'fa-flask'),
        (66, 'Plumbing & Pipe Fitting', 0, 'fa-book'),
        (67, 'Principles of Cost Accounting', 0, 'fa-book'),
        (68, 'Printing Craft Practice', 0, 'fa-book'),
        (69, 'Radio, Television & Electronic Works', 0, 'fa-book'),
        (70, 'Salesmanship', 0, 'fa-book'),
        (71, 'Stenography', 0, 'fa-book'),
        (72, 'Store Keeping', 0, 'fa-book'),
        (73, 'Store Management', 0, 'fa-book'),
        (74, 'Technical Drawing', 0, 'fa-book'),
        (75, 'Tourism', 0, 'fa-book'),
        (76, 'Upholstery', 0, 'fa-book'),
        (77, 'Visual Art', 0, 'fa-paintbrush'),
        (78, 'Welding & Fabrication Engineering Craft', 0, 'fa-book'),
        (79, 'Woodwork', 0, 'fa-book'),
        (80, 'Yoruba', 0, 'fa-language')
    ]
    
    for order, name, practical, icon in waec_subjects:
        # Check if subject already exists
        cursor.execute("SELECT id FROM subjects WHERE name = ? AND exam_type = 'WAEC'", (name,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO subjects (name, exam_type, has_practical, icon, display_order, show_on_homepage)
                VALUES (?, 'WAEC', ?, ?, ?, 1)
            ''', (name, practical, icon, order))
            print(f"  Added: {name}")
        else:
            print(f"  ⏭️ Already exists: {name}")
    
    print("✅ All 80 WAEC subjects verified!")

# Show final counts
print("\n" + "=" * 50)
print("FINAL DATABASE STATUS")
print("=" * 50)

cursor.execute("SELECT COUNT(*) FROM subjects WHERE exam_type = 'WAEC'")
waec_count = cursor.fetchone()[0]
print(f"📚 WAEC Subjects: {waec_count}")

cursor.execute("SELECT COUNT(*) FROM subjects")
print(f"📚 Total Subjects: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM home_content")
print(f"📝 Home Content Sections: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM site_settings")
print(f"⚙️ Site Settings: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM pins")
print(f"🔑 Total PINs: {cursor.fetchone()[0]}")

# Commit and close
conn.commit()
conn.close()

print("\n" + "=" * 50)
print("✅ Database migration completed successfully!")
print("=" * 50)