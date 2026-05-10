from app import create_app, db
from app.models import Pin
import sqlite3
import os

app = create_app()

def add_column_if_not_exists():
    db_path = 'instance/answerpoint.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if answer_text_color column exists
    cursor.execute("PRAGMA table_info(pins)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'answer_text_color' not in columns:
        print("Adding answer_text_color column to pins table...")
        cursor.execute("ALTER TABLE pins ADD COLUMN answer_text_color VARCHAR(7) DEFAULT '#1f2937'")
        conn.commit()
        print("✅ answer_text_color column added successfully!")
    else:
        print("✅ answer_text_color column already exists")
    
    # Also check for text_color column (if you want to keep both or migrate)
    if 'text_color' in columns and 'answer_text_color' in columns:
        print("Migrating data from text_color to answer_text_color...")
        cursor.execute("UPDATE pins SET answer_text_color = text_color WHERE answer_text_color IS NULL AND text_color IS NOT NULL")
        conn.commit()
        print("✅ Data migrated!")
    
    conn.close()

with app.app_context():
    print("Checking database schema...")
    add_column_if_not_exists()
    
    # Verify the column exists now
    print("\nVerifying columns:")
    conn = sqlite3.connect('instance/answerpoint.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(pins)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]}: {col[2]}")
    conn.close()
    
    print("\n✅ Database update complete!")
