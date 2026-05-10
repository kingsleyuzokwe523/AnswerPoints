#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, '/home/Answerpoint/AnswerPoint')

from app import create_app, db
import sqlite3

app = create_app()
with app.app_context():
    db_path = 'instance/answerpoint.db'
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(pins)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print("Existing columns:", columns)
        
        if 'subject_name' not in columns:
            cursor.execute("ALTER TABLE pins ADD COLUMN subject_name VARCHAR(200)")
            print("Added subject_name column")
        
        if 'main_title' not in columns:
            cursor.execute("ALTER TABLE pins ADD COLUMN main_title VARCHAR(500) DEFAULT 'OFFICIAL ANSWERS'")
            print("Added main_title column")
        
        if 'is_active' not in columns:
            cursor.execute("ALTER TABLE pins ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("Added is_active column")
        
        conn.commit()
        conn.close()
        print("Database updated successfully!")
    else:
        print("Creating database...")
        db.create_all()
        print("Database created!")
