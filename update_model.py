# Run this to update the Pin model
python3 -c "
from app import db
from app.models import Pin
import os

# Read the models file
models_path = 'app/models.py'
with open(models_path, 'r') as f:
    content = f.read()

# Remove created_at line from Pin class
import re
pattern = r'    created_at = db\.Column\(db\.DateTime, default=datetime\.utcnow\)\n'
if 'created_at' in content:
    content = re.sub(pattern, '', content)
    with open(models_path, 'w') as f:
        f.write(content)
    print('✅ removed created_at from Pin model')
else:
    print('created_at not found in Pin model')

print('Model updated successfully!')
"
