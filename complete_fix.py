import sqlite3
import os

db_path = 'instance/answerpoint.db'

print("🔧 Starting complete database fix...")
print("=" * 50)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Fix home_content table - add missing columns
print("\n1. Fixing home_content table...")
cursor.execute("PRAGMA table_info(home_content)")
columns = [col[1] for col in cursor.fetchall()]

if 'content_type' not in columns:
    print("   Adding content_type column...")
    cursor.execute("ALTER TABLE home_content ADD COLUMN content_type VARCHAR(50) DEFAULT 'text'")
    print("   ✅ Added content_type")

# 2. Fix site_settings table
print("\n2. Fixing site_settings table...")
cursor.execute("PRAGMA table_info(site_settings)")
columns = [col[1] for col in cursor.fetchall()]

if 'description' not in columns:
    print("   Adding description column...")
    cursor.execute("ALTER TABLE site_settings ADD COLUMN description TEXT")
    print("   ✅ Added description")

# 3. Check pins table structure
print("\n3. Verifying pins table...")
cursor.execute("PRAGMA table_info(pins)")
columns = cursor.fetchall()
print("   Current columns:")
for col in columns:
    print(f"   - {col[1]}: {col[2]}")

# 4. Insert default home content if empty
print("\n4. Inserting default home content...")
cursor.execute("SELECT COUNT(*) FROM home_content")
count = cursor.fetchone()[0]

if count == 0:
    default_content = [
        ('hero_title', 'Welcome to AnswerPoint', 'text'),
        ('hero_text', 'Your #1 Source for Exam Answers', 'text'),
        ('moving_tagline', 'Excellence in Education', 'text'),
        ('whatsapp_link', 'https://wa.me/1234567890', 'url'),
        ('telegram_link', 'https://t.me/answerpoint', 'url'),
        ('vip_text', 'VIP Support', 'text'),
        ('vip_number', '+1234567890', 'text'),
        ('support_email', 'support@answerpoint.com', 'email'),
        ('footer_text', '© 2024 AnswerPoint. All rights reserved.', 'text'),
    ]
    
    for section, content, content_type in default_content:
        cursor.execute(
            "INSERT INTO home_content (section, content, content_type) VALUES (?, ?, ?)",
            (section, content, content_type)
        )
    print(f"   ✅ Inserted {len(default_content)} default records")
else:
    print(f"   ✅ Found {count} existing records")

# 5. Insert default site settings
print("\n5. Inserting default site settings...")
cursor.execute("SELECT COUNT(*) FROM site_settings")
count = cursor.fetchone()[0]

if count == 0:
    default_settings = [
        ('site_name', 'AnswerPoint', 'Site name'),
        ('admin_email', 'admin@answerpoint.com', 'Admin email'),
        ('waec_timetable_text', 'WAEC Timetable will be posted soon', 'WAEC timetable'),
        ('neco_timetable_text', 'NECO Timetable will be posted soon', 'NECO timetable'),
    ]
    
    for key, value, desc in default_settings:
        cursor.execute(
            "INSERT INTO site_settings (setting_key, setting_value, description) VALUES (?, ?, ?)",
            (key, value, desc)
        )
    print(f"   ✅ Inserted {len(default_settings)} default settings")
else:
    print(f"   ✅ Found {count} existing settings")

# 6. Verify all tables are working
print("\n6. Verifying all tables...")
tables = ['pins', 'subjects', 'images', 'home_content', 'site_settings']
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"   ✅ {table}: {count} records")

conn.commit()
conn.close()

print("\n" + "=" * 50)
print("🎉 Database fix complete!")
print("=" * 50)
