from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
import uuid

# Initialisiere Flask App
app = Flask(__name__)
app.secret_key = 'dein_secret_key'

# Datenbank-Konfiguration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['UPLOAD_FOLDER'] = 'static/Profilbild'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Sicherstellen, dass der Upload-Ordner existiert
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Standard-Profilbild Name
DEFAULT_PROFILE_PICTURE = "Standartprofilbild.png"

# User-Datenbankmodell
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150), default=DEFAULT_PROFILE_PICTURE)
    is_profile_complete = db.Column(db.Boolean, default=False)

# Post-Datenbankmodell
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    emotion = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=True)  
    longitude = db.Column(db.Float, nullable=True) 

# Erstelle die Datenbank, falls sie nicht existiert
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    if 'Angemeldet' in session:
        return render_template('Hauptseite.html', Angemeldet=True, username=session.get('username'))
    return render_template('Hauptseite.html', Angemeldet=False)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if 'Angemeldet' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['Angemeldet'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('Login.html', error="Ungültiger Benutzername oder Passwort")

    return render_template('Login.html')

@app.route('/Registrieren', methods=['GET', 'POST'])
def register():
    if 'Angemeldet' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('Registrieren.html', error="Benutzername existiert bereits")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, profile_picture=DEFAULT_PROFILE_PICTURE)
        db.session.add(new_user)
        db.session.commit()

        session['Angemeldet'] = True
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('Registrieren.html')

@app.route('/Logout')
def logout():
    session.pop('Angemeldet', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/Profil', methods=['GET', 'POST'])
def profile():
    if 'Angemeldet' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        user.gender = request.form.get('gender')
        user.age = request.form.get('age')
        user.email = request.form.get('email')

        file = request.files.get('profile_picture')
        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Falls bereits ein Profilbild existiert und nicht das Standardbild ist, löschen
            if user.profile_picture and user.profile_picture != DEFAULT_PROFILE_PICTURE:
                old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)

            file.save(filepath)
            user.profile_picture = filename 

        db.session.commit() 

        return redirect(url_for('profile'))

    return render_template('Profil.html', user=user)

@app.route('/Profil/Löschen', methods=['POST'])
def delete_profile_picture():
    if 'Angemeldet' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()

    if user.profile_picture and user.profile_picture != DEFAULT_PROFILE_PICTURE:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
        if os.path.exists(file_path):
            os.remove(file_path)  # Lösche das aktuelle Profilbild

    # Setze das Profilbild auf das Standardbild zurück
    user.profile_picture = DEFAULT_PROFILE_PICTURE
    db.session.commit()

    return redirect(url_for('profile'))

@app.route('/Post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        file = request.files.get('file')
        description = request.form.get('description')
        emotion = request.form.get('emotion')
        latitude = request.form.get('latitude')  
        longitude = request.form.get('longitude')

        if latitude == '':
            latitude = None
        if longitude == '':
            longitude = None

        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_post = Post(image_file=filename, description=description, emotion=emotion, latitude=latitude, longitude=longitude)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('feed'))

    return render_template('Post.html')

@app.route('/Feed')
def feed():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('Feed.html', posts=posts)

if __name__ == "__main__":
    app.run(debug=True)