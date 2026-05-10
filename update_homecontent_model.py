# Update HomeContent model to include content_type
python3 -c "
import re

with open('app/models.py', 'r') as f:
    content = f.read()

# Check if HomeContent class has content_type
if 'content_type' not in content:
    # Add content_type to HomeContent class
    pattern = r'(class HomeContent\(db\.Model\):.*?)(\n    )'
    
    new_field = '\n    content_type = db.Column(db.String(50), default=\'text\')'
    
    if 'content_type' not in content:
        # Find where to insert
        lines = content.split('\n')
        new_lines = []
        in_homecontent = False
        
        for line in lines:
            if 'class HomeContent(db.Model):' in line:
                in_homecontent = True
                new_lines.append(line)
                continue
            
            if in_homecontent and 'content = db.Column' in line:
                new_lines.append(line)
                new_lines.append('    content_type = db.Column(db.String(50), default=\'text\')')
                continue
                
            if in_homecontent and line.strip() and not line.startswith(' ') and line.strip():
                in_homecontent = False
                
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open('app/models.py', 'w') as f:
            f.write(content)
        print('✅ Added content_type to HomeContent model')
    else:
        print('✅ content_type already exists')
else:
    print('✅ content_type already in model')
"
