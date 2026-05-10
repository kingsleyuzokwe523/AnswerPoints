import sqlite3
import os

# Connect to the database
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
        print(f"Error: {e}")

# 2. Add icon column to subjects
try:
    cursor.execute("ALTER TABLE subjects ADD COLUMN icon TEXT DEFAULT 'fa-book'")
    print("✅ Added icon column to subjects")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ icon column already exists")
    else:
        print(f"Error: {e}")

# 3. Add show_on_homepage column to subjects
try:
    cursor.execute("ALTER TABLE subjects ADD COLUMN show_on_homepage BOOLEAN DEFAULT 1")
    print("✅ Added show_on_homepage column to subjects")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⏭️ show_on_homepage column already exists")
    else:
        print(f"Error: {e}")

# 4. Create site_settings table if not exists
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            setting_type TEXT DEFAULT 'text'
        )
    ''')
    print("✅ site_settings table ready")
except sqlite3.OperationalError as e:
    print(f"Error creating site_settings: {e}")

# 5. Add default home content sections if missing
default_sections = [
    ('hero_title', 'AnswerPoint 2026'),
    ('hero_text', 'Your reliable source for correct WAEC, NECO, and JAMB answers'),
    ('moving_tagline', '🔥 100% VERIFIED WAEC & NECO ANSWERS — JOIN OUR FREE WHATSAPP & TELEGRAM CHANNELS! 🔥'),
    ('announcement', '2026 WAEC/NECO Examinations are underway!'),
    ('instructions', 'Enter your 3-digit PIN to get verified answers'),
    ('hot_updates_text', '2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE'),
    ('whatsapp_link', 'https://whatsapp.com/channel/yourlink'),
    ('telegram_link', 'https://t.me/yourchannel'),
    ('vip_text', 'Want early VIP answers before the exam?'),
    ('vip_number', '08065582389'),
    ('need_help_text', 'Need Help or Updates? → Join Our Official WhatsApp & Telegram Channels Today!'),
    ('footer_text', '© 2026 AnswerPoint - Your Exam Success Partner')
]

for section, content in default_sections:
    try:
        cursor.execute(
            "INSERT INTO home_content (section, content, content_type) VALUES (?, ?, ?)",
            (section, content, 'text')
        )
        print(f"✅ Added: {section}")
    except sqlite3.IntegrityError:
        print(f"⏭️ Already exists: {section}")

# 6. Add default site settings
default_settings = [
    ('site_name', 'AnswerPoint'),
    ('admin_email', 'support@answerpoint.com'),
    ('primary_color', '#1e40af'),
    ('secondary_color', '#dc2626')
]

for key, value in default_settings:
    try:
        cursor.execute(
            "INSERT INTO site_settings (setting_key, setting_value, setting_type) VALUES (?, ?, ?)",
            (key, value, 'text')
        )
        print(f"✅ Added setting: {key}")
    except sqlite3.IntegrityError:
        print(f"⏭️ Setting already exists: {key}")

# 7. Update existing subjects with default icons
cursor.execute("UPDATE subjects SET icon = 'fa-book' WHERE icon IS NULL")
print("✅ Updated subject icons")

# Commit changes
conn.commit()
conn.close()

print("=" * 50)
print("Database migration completed successfully!")
print("=" * 50)