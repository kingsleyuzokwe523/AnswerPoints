import re

with open('app/database.py', 'r') as f:
    content = f.read()

print("Fixing database.py...")

# Fix HomeContent creation to include content_type
old_code = "HomeContent(section=key, content=value)"
new_code = "HomeContent(section=key, content=value, content_type='text')"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('app/database.py', 'w') as f:
        f.write(content)
    print("✅ Updated HomeContent creation in database.py")
else:
    print("⚠️ Could not find the code to replace")
    
# Also fix any other HomeContent creations
old_code2 = "HomeContent(section=section, content=content)"
new_code2 = "HomeContent(section=section, content=content, content_type='text')"

if old_code2 in content:
    content = content.replace(old_code2, new_code2)
    with open('app/database.py', 'w') as f:
        f.write(content)
    print("✅ Updated second instance")

print("\n✅ database.py fix complete")
