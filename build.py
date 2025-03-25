import os
import shutil

# Create public directory if it doesn't exist
if not os.path.exists('public'):
    os.makedirs('public')

# Copy static files
if os.path.exists('static'):
    shutil.copytree('static', 'public/static', dirs_exist_ok=True)

# Copy templates
if os.path.exists('templates'):
    shutil.copytree('templates', 'public/templates', dirs_exist_ok=True)

# Copy app.py
shutil.copy2('app.py', 'public/app.py')

# Copy requirements.txt
shutil.copy2('requirements.txt', 'public/requirements.txt')

# Create a simple index.html that will serve as the entry point
with open('public/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
    <meta http-equiv="refresh" content="0;url=/app.py">
</head>
<body>
    <p>Redirecting to URL Shortener...</p>
</body>
</html>
    ''')

print("Build completed successfully!") 