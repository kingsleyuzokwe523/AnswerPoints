import re

# Read the models file
with open('app/models.py', 'r') as f:
    content = f.read()

# Check if HomeContent class has content_type
if 'content_type' not in content:
    print("Adding content_type to HomeContent model...")
    
    # Find where to insert
    lines = content.split('\n')
    new_lines = []
    in_homecontent = False
    inserted = False
    
    for line in lines:
        if 'class HomeContent(db.Model):' in line:
            in_homecontent = True
            new_lines.append(line)
            continue
        
        if in_homecontent and not inserted and 'content = db.Column' in line:
            new_lines.append(line)
            new_lines.append('    content_type = db.Column(db.String(50), default=\'text\')')
            inserted = True
            continue
            
        if in_homecontent and line.strip() and not line.startswith(' ') and 'class ' in line:
            in_homecontent = False
            
        new_lines.append(line)
    
    if inserted:
        content = '\n'.join(new_lines)
        with open('app/models.py', 'w') as f:
            f.write(content)
        print("✅ Added content_type to HomeContent model")
    else:
        print("⚠️ Could not find where to insert content_type")
else:
    print("✅ content_type already exists in HomeContent model")

# Verify
print("\nVerifying HomeContent class:")
with open('app/models.py', 'r') as f:
    for line in f:
        if 'class HomeContent' in line or 'content_type' in line:
            print(f"  {line.strip()}")
