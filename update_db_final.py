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
        
        # Check existing columns in pins table
        cursor.execute("PRAGMA table_info(pins)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print("=" * 50)
        print("Existing columns in 'pins' table:")
        print(columns)
        print("=" * 50)
        
        # Add missing columns one by one
        columns_to_add = [
            ('subject_name', 'VARCHAR(200)'),
            ('main_title', 'VARCHAR(500) DEFAULT "OFFICIAL ANSWERS"'),
            ('is_active', 'BOOLEAN DEFAULT 1'),
            ('posted_by', 'VARCHAR(200) DEFAULT "AnswerPoint"'),
            ('header_color', 'VARCHAR(7) DEFAULT "#ffffff"')
        ]
        
        for col_name, col_type in columns_to_add:
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE pins ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Added column: {col_name}")
                except Exception as e:
                    print(f"❌ Error adding {col_name}: {e}")
            else:
                print(f"⚠️ Column '{col_name}' already exists")
        
        conn.commit()
        
        # Verify all columns now exist
        cursor.execute("PRAGMA table_info(pins)")
        updated_columns = [col[1] for col in cursor.fetchall()]
        
        print("\n" + "=" * 50)
        print("Updated columns in 'pins' table:")
        print(updated_columns)
        print("=" * 50)
        
        conn.close()
        print("\n✅ Database updated successfully!")
    else:
        print("Creating new database...")
        db.create_all()
        print("✅ Database created!")
