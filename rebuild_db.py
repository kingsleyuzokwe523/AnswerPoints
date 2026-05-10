import sqlite3
import os

db_path = 'instance/answerpoint.db'

# Backup and remove old database
if os.path.exists(db_path):
    os.rename(db_path, f'{db_path}.old_backup')
    print(f"✅ Backed up old database to {db_path}.old_backup")

# Create new database and run migrations
from app import create_app, db

print("Creating new database...")
app = create_app()

with app.app_context():
    db.create_all()
    print("✅ All tables created")
    
    # Insert default data
    from app.database import init_default_data
    init_default_data()
    print("✅ Default data inserted")
    
    # Verify
    from app.models import HomeContent, SiteSettings, Subject, Pin
    
    print(f"\nVerification:")
    print(f"  HomeContent: {HomeContent.query.count()} records")
    print(f"  SiteSettings: {SiteSettings.query.count()} records")
    print(f"  Subjects: {Subject.query.count()} records")
    print(f"  Pins: {Pin.query.count()} records")
    
    print("\n🎉 Database rebuilt successfully!")
