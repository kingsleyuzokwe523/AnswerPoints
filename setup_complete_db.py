import sqlite3
import os
from werkzeug.security import generate_password_hash

# Delete old database
db_path = 'instance/answerpoint.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old database deleted")

# Create new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create admins table
cursor.execute('''
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP
)
''')

# Create subjects table
cursor.execute('''
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    exam_type TEXT NOT NULL,
    has_practical INTEGER DEFAULT 0,
    display_order INTEGER DEFAULT 0
)
''')

# Create pins table
cursor.execute('''
CREATE TABLE pins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_code TEXT UNIQUE NOT NULL,
    subject_id INTEGER NOT NULL,
    answer_text TEXT,
    created_at TIMESTAMP,
    views INTEGER DEFAULT 0,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
)
''')

# Create images table
cursor.execute('''
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    uploaded_at TIMESTAMP,
    FOREIGN KEY (pin_id) REFERENCES pins (id)
)
''')

# Create home_content table
cursor.execute('''
CREATE TABLE home_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT UNIQUE NOT NULL,
    content TEXT
)
''')

# Create exam_timetables table
cursor.execute('''
CREATE TABLE exam_timetables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    paper TEXT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    year INTEGER DEFAULT 2026
)
''')

print("Tables created")

# Insert admin
cursor.execute(
    "INSERT INTO admins (username, password, created_at) VALUES (?, ?, datetime('now'))",
    ('admin', generate_password_hash('admin123'))
)
print("Admin created: admin / admin123")

# Insert home content
home_data = [
    ('hero_title', 'AnswerPoint 2026'),
    ('hero_text', 'Your reliable source for WAEC & NECO exam answers. Get verified solutions and excel in your examinations.'),
    ('announcement', '📢 HOT: 2026 WAEC/NECO Examinations are underway! Get your PIN from admin for verified answers.'),
    ('instructions', '📌 HOW TO USE AnswerPoint:\n\n1️⃣ Get your unique 3-digit PIN from your administrator\n2️⃣ Enter the PIN in the box above\n3️⃣ Click "See Answer" to view the solution\n4️⃣ Study the answers and succeed!'),
    ('whatsapp_link', 'https://whatsapp.com/channel/yourlink'),
    ('telegram_link', 'https://t.me/yourchannel'),
    ('footer_text', '© 2026 AnswerPoint - Your Exam Success Partner | WAEC & NECO Answers Portal')
]

for section, content in home_data:
    cursor.execute("INSERT INTO home_content (section, content) VALUES (?, ?)", (section, content))
print("Home content added")

# Insert sample subjects
all_subjects = [
    "Mathematics", "English Language", "Physics", "Chemistry", "Biology",
    "Economics", "Government", "Geography", "Commerce", "Accounts",
    "Literature in English", "Christian Religious Studies", "Islamic Studies",
    "History", "Further Mathematics", "Civic Education", "Data Processing",
    "Computer Studies", "Agricultural Science"
]

practical_subjects = ["Physics", "Chemistry", "Biology", "Agricultural Science", "Computer Studies"]

# Add WAEC subjects
for name in all_subjects:
    has_practical = 1 if name in practical_subjects else 0
    cursor.execute(
        "INSERT INTO subjects (name, exam_type, has_practical) VALUES (?, ?, ?)",
        (name, 'WAEC', has_practical)
    )

# Add NECO subjects
for name in all_subjects:
    has_practical = 1 if name in practical_subjects else 0
    cursor.execute(
        "INSERT INTO subjects (name, exam_type, has_practical) VALUES (?, ?, ?)",
        (name, 'NECO', has_practical)
    )
print(f"Subjects added: {len(all_subjects) * 2} subjects")

# Get Mathematics subject ID for sample PIN
cursor.execute("SELECT id FROM subjects WHERE name='Mathematics' AND exam_type='WAEC'")
math_id = cursor.fetchone()[0]

# Insert sample PIN
cursor.execute(
    "INSERT INTO pins (pin_code, subject_id, answer_text, created_at, views) VALUES (?, ?, ?, datetime('now'), 0)",
    ('123', math_id, '📚 MATHEMATICS ANSWER:\n\nQuestion: Solve for x in the equation 2x + 5 = 13\n\nSolution:\n2x + 5 = 13\n2x = 13 - 5\n2x = 8\nx = 4\n\n✅ Final Answer: x = 4')
)
print("Sample PIN 123 created")

# Insert sample timetable
timetable = [
    ("WAEC", "Mathematics", "Paper 1 & 2", "May 15th, 2026", "9:00 AM - 1:00 PM"),
    ("WAEC", "English Language", "Paper 1 & 2", "May 16th, 2026", "9:00 AM - 12:30 PM"),
    ("WAEC", "Physics", "Theory & Objective", "May 18th, 2026", "9:00 AM - 12:00 PM"),
]

for exam_type, subject, paper, date, time in timetable:
    cursor.execute(
        "INSERT INTO exam_timetables (exam_type, subject, paper, date, time, year) VALUES (?, ?, ?, ?, ?, ?)",
        (exam_type, subject, paper, date, time, 2026)
    )
print("Timetable entries added")

conn.commit()
conn.close()

print("=" * 50)
print("✅ DATABASE SETUP COMPLETE!")
print("👤 Admin: admin / admin123")
print("🔑 Sample PIN: 123 (Mathematics)")
print("=" * 50)