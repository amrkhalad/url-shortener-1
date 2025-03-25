from flask import Flask, render_template, request, redirect, url_for, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
import random
import string
import validators # type: ignore
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder=os.path.abspath('templates'),
            static_folder=os.path.abspath('static') if os.path.exists('static') else None)

# Use environment variable for database URL or fallback to SQLite
database_url = os.getenv('DATABASE_URL', 'sqlite:///urls.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400
    
    custom_code = data.get('custom_code')
    if custom_code:
        if URL.query.filter_by(short_code=custom_code).first():
            return jsonify({'error': 'Custom code already exists'}), 400
        short_code = custom_code
    else:
        short_code = generate_short_code()
    
    short_code = f"{short_code}zageng"
    
    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    
    return jsonify({
        'short_url': f"{request.host_url}{short_code}",
        'original_url': original_url
    })

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.visits += 1
        db.session.commit()
        return redirect(url.original_url)
    return render_template('404.html'), 404

@app.route('/api/stats/<short_code>')
def get_url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return jsonify({
            'original_url': url.original_url,
            'visits': url.visits,
            'created_at': url.created_at.isoformat()
        })
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 