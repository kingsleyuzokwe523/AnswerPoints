import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# Create instance folder
os.makedirs('instance', exist_ok=True)

# Connect to database
conn = sqlite3.connect('instance/answerpoint.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    exam_type TEXT NOT NULL,
    has_practical BOOLEAN DEFAULT 0,
    display_order INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_code TEXT UNIQUE NOT NULL,
    subject_id INTEGER NOT NULL,
    answer_text TEXT,
    created_at TIMESTAMP,
    views INTEGER DEFAULT 0,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    uploaded_at TIMESTAMP,
    FOREIGN KEY (pin_id) REFERENCES pins (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS home_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT UNIQUE NOT NULL,
    content TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS exam_timetables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    paper TEXT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    year INTEGER DEFAULT 2026
)
''')

# Insert default admin
cursor.execute('''
INSERT INTO admins (username, password, created_at)
VALUES (?, ?, ?)
''', ('admin', generate_password_hash('admin123'), datetime.now()))

# Insert default home content
default_content = [
    ('hero_title', 'AnswerPoint 2026'),
    ('hero_text', 'Your reliable source for accurate WAEC & NECO exam answers.'),
    ('announcement', '📢 2026 WAEC/NECO Examinations are underway!'),
    ('instructions', 'Enter your 3-digit PIN to get answers.'),
    ('whatsapp_link', 'https://whatsapp.com/channel/yourlink'),
    ('telegram_link', 'https://t.me/yourchannel'),
    ('footer_text', '© 2026 AnswerPoint - Your Exam Success Partner')
]

for section, content in default_content:
    cursor.execute('INSERT INTO home_content (section, content) VALUES (?, ?)', (section, content))

# Insert sample subjects
subjects = [
    ("Mathematics", "WAEC", 0),
    ("English Language", "WAEC", 0),
    ("Physics", "WAEC", 1),
    ("Chemistry", "WAEC", 1),
    ("Biology", "WAEC", 1),
]

for name, exam_type, has_practical in subjects:
    cursor.execute('''
    INSERT INTO subjects (name, exam_type, has_practical)
    VALUES (?, ?, ?)
    ''', (name, exam_type, has_practical))

# Insert sample PINs
cursor.execute('INSERT INTO pins (pin_code, subject_id, answer_text, created_at, views) VALUES (?, ?, ?, ?, ?)',
               ('123', 1, 'Mathematics Answer: \n\nStep 1: Solve equation\nStep 2: Final answer = 42', datetime.now(), 0))

conn.commit()
conn.close()

print("✅ Database created successfully!")
print("👤 Admin: admin / admin123")
print("🔑 Sample PIN: 123")
