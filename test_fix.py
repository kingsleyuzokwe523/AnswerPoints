from app import create_app, db
from app.models import Pin, Subject, HomeContent, SiteSettings

try:
    print("Creating app...")
    app = create_app()
    
    with app.app_context():
        print("✅ App created successfully")
        
        # Test HomeContent
        print(f"\nHomeContent records: {HomeContent.query.count()}")
        home_records = HomeContent.query.all()
        for record in home_records[:3]:
            print(f"  - {record.section}: {record.content[:50]}...")
        
        # Test Pins
        print(f"\nPins: {Pin.query.count()}")
        pins = Pin.query.all()
        for pin in pins:
            print(f"  - PIN: {pin.pin_code}, Subject: {pin.subject_name}")
        
        # Test Subjects
        print(f"\nSubjects: {Subject.query.count()}")
        
        # Test SiteSettings
        print(f"SiteSettings: {SiteSettings.query.count()}")
        
        print("\n🎉 All database tests passed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
