import sqlite3
import os

db_path = 'instance/answerpoint.db'

# Backup existing database
if os.path.exists(db_path):
    os.rename(db_path, f'{db_path}.backup')
    print(f"✅ Backed up old database to {db_path}.backup")

# Create new database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create pins table without created_at issues
cursor.execute('''
CREATE TABLE IF NOT EXISTS pins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_code VARCHAR(3) NOT NULL UNIQUE,
    subject_id INTEGER,
    subject_name VARCHAR(200),
    main_title VARCHAR(500) DEFAULT 'OFFICIAL ANSWERS',
    posted_by VARCHAR(200) DEFAULT 'AnswerPoint',
    header_color VARCHAR(7) DEFAULT '#ffffff',
    answer_text TEXT,
    is_active BOOLEAN DEFAULT 1,
    views INTEGER DEFAULT 0,
    text_color VARCHAR(7) DEFAULT '#1f2937',
    answer_text_color VARCHAR(7) DEFAULT '#1f2937',
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
)
''')

print("✅ Created pins table without created_at")

# Create subjects table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL UNIQUE,
    exam_type VARCHAR(20) DEFAULT 'WAEC',
    has_practical BOOLEAN DEFAULT 0,
    icon VARCHAR(50) DEFAULT 'fa-book',
    show_on_homepage BOOLEAN DEFAULT 1,
    display_order INTEGER DEFAULT 0
)
''')

print("✅ Created subjects table")

# Create images table
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_id INTEGER NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(200),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pin_id) REFERENCES pins (id) ON DELETE CASCADE
)
''')

print("✅ Created images table")

# Create home_content table
cursor.execute('''
CREATE TABLE IF NOT EXISTS home_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section VARCHAR(100) NOT NULL UNIQUE,
    content TEXT
)
''')

print("✅ Created home_content table")

# Create site_settings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS site_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT
)
''')

print("✅ Created site_settings table")

# Insert default subjects
subjects = [
    ('MATHEMATICS', 'WAEC', 0, 'fa-calculator'),
    ('ENGLISH LANGUAGE', 'WAEC', 0, 'fa-book'),
    ('PHYSICS', 'WAEC', 1, 'fa-flask'),
    ('CHEMISTRY', 'WAEC', 1, 'fa-flask'),
    ('BIOLOGY', 'WAEC', 1, 'fa-leaf'),
]

for subject in subjects:
    cursor.execute('''
    INSERT OR IGNORE INTO subjects (name, exam_type, has_practical, icon)
    VALUES (?, ?, ?, ?)
    ''', subject)

print("✅ Inserted default subjects")

# Insert a test PIN
cursor.execute('''
INSERT OR IGNORE INTO pins (pin_code, subject_name, posted_by, header_color, answer_text, answer_text_color, text_color)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', ('123', 'MATHEMATICS', 'AnswerPoint', '#ffffff', '<p>Test answer content here</p>', '#1f2937', '#1f2937'))

print("✅ Inserted test PIN")

conn.commit()
conn.close()

print("\n🎉 Database reset complete!")
print("=" * 50)
print("New tables created without created_at column issues")
print("Test PIN created: 123 - MATHEMATICS")
print("=" * 50)
