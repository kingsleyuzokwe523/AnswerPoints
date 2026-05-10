#!/usr/bin/env python3
from app import create_app, db
from app.models import Subject, Pin, HomeContent, SiteSettings, Admin

app = create_app()
with app.app_context():
    # Initialize database
    db.create_all()
    
    # Check what exists
    subjects = Subject.query.count()
    pins = Pin.query.count()
    home = HomeContent.query.count()
    settings = SiteSettings.query.count()
    admin = Admin.query.count()
    
    print(f"📊 Database Status:")
    print(f"   Subjects: {subjects}")
    print(f"   PINs: {pins}")
    print(f"   Home Content: {home}")
    print(f"   Site Settings: {settings}")
    print(f"   Admins: {admin}")
    
    # If no subjects, add a few sample ones
    if subjects == 0:
        print("\n📚 No subjects found. Adding sample subjects...")
        sample_subjects = [
            Subject(name="Mathematics", exam_type="WAEC", has_practical=False, display_order=1, icon="fa-calculator"),
            Subject(name="English Language", exam_type="WAEC", has_practical=False, display_order=2, icon="fa-book"),
            Subject(name="Physics", exam_type="WAEC", has_practical=True, display_order=3, icon="fa-flask"),
            Subject(name="Chemistry", exam_type="WAEC", has_practical=True, display_order=4, icon="fa-flask"),
            Subject(name="Biology", exam_type="WAEC", has_practical=True, display_order=5, icon="fa-microscope"),
        ]
        for subj in sample_subjects:
            db.session.add(subj)
        db.session.commit()
        print(f"   ✅ Added {len(sample_subjects)} sample subjects")
    
    print("\n✅ Database check complete!")
