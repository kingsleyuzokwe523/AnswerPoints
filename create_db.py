import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Create instance folder
os.makedirs('instance', exist_ok=True)

# Delete old database if exists
if os.path.exists('instance/answerpoint.db'):
    os.remove('instance/answerpoint.db')

# Create database
conn = sqlite3.connect('instance/answerpoint.db')
cursor = conn.cursor()

# Create tables
cursor.execute('CREATE TABLE admins (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
cursor.execute('CREATE TABLE subjects (id INTEGER PRIMARY KEY, name TEXT, exam_type TEXT, has_practical INTEGER)')
cursor.execute('CREATE TABLE pins (id INTEGER PRIMARY KEY, pin_code TEXT, subject_id INTEGER, answer_text TEXT, views INTEGER)')
cursor.execute('CREATE TABLE images (id INTEGER PRIMARY KEY, pin_id INTEGER, image_path TEXT)')
cursor.execute('CREATE TABLE home_content (id INTEGER PRIMARY KEY, section TEXT, content TEXT)')
cursor.execute('CREATE TABLE exam_timetables (id INTEGER PRIMARY KEY, exam_type TEXT, subject TEXT, paper TEXT, date TEXT, time TEXT)')

# Add admin
cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('admin', generate_password_hash('admin123')))

# Add home content
cursor.execute("INSERT INTO home_content (section, content) VALUES (?, ?)", ('hero_title', 'AnswerPoint 2026'))
cursor.execute("INSERT INTO home_content (section, content) VALUES (?, ?)", ('hero_text', 'Your reliable source for WAEC & NECO answers'))
cursor.execute("INSERT INTO home_content (section, content) VALUES (?, ?)", ('announcement', '2026 Examinations are underway'))
cursor.execute("INSERT INTO home_content (section, content) VALUES (?, ?)", ('instructions', 'Enter your 3-digit PIN to get answers'))

# Add sample subject
cursor.execute("INSERT INTO subjects (name, exam_type, has_practical) VALUES (?, ?, ?)", ('Mathematics', 'WAEC', 0))

# Get subject id
cursor.execute("SELECT id FROM subjects WHERE name='Mathematics'")
math_id = cursor.fetchone()[0]

# Add sample PIN
cursor.execute("INSERT INTO pins (pin_code, subject_id, answer_text, views) VALUES (?, ?, ?, ?)", ('123', math_id, 'Answer for Mathematics', 0))

conn.commit()
conn.close()

print("=" * 50)
print("DATABASE CREATED SUCCESSFULLY!")
print("Admin: admin / admin123")
print("Sample PIN: 123")
print("=" * 50)
