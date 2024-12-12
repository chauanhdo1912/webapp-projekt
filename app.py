from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

# Diese Funktion erstellt die SQLite-Datenbank und die Tabelle
def init_db():
    if not os.path.exists('Nutzer.db'):
        conn = sqlite3.connect('Nutzer.db')  # Diese Zeile erstellt die Datei, wenn sie noch nicht existiert
        cursor = conn.cursor()
        
        # Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Datenbank und Tabelle wurden erfolgreich erstellt.")
    else:
        print("Datenbank existiert bereits.")

# Datenbank initialisieren
init_db()

app = Flask(__name__)
app.secret_key = 'dein_secret_key' 

basedir = os.path.abspath(os.path.dirname(__file__))  # Root file
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "posts.db")}'
app.config['UPLOAD_FOLDER'] = 'static/images'  
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} 
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Post('{self.image_file}', '{self.description}')"
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def Home():
    if 'Angemeldet' in session:  # Benutzer ist angemeldet
        return render_template('Hauptseite.html', Angemeldet=True, username=session.get('username'))
    return render_template('Hauptseite.html', Angemeldet=False)  # Benutzer ist nicht angemeldet

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if 'Angemeldet' in session:  # Wenn der Benutzer schon eingeloggt ist
        return redirect(url_for('Home'))
    
    if request.method == 'POST':  # Wenn das Formular abgesendet wird
        username = request.form['username']
        password = request.form['password']
     
        conn = sqlite3.connect('Nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()  # Nur ein Ergebnis zurückholen
        conn.close()

        if result:  # Wenn der Benutzer existiert
            stored_password = result[0]  # Das gespeicherte Passwort holen
            if check_password_hash(stored_password, password):  # Passwort überprüfen
                session['Angemeldet'] = True
                session['username'] = username
                return redirect(url_for('Home'))  # Zur Hauptseite weiterleiten
            else:
                return render_template('Login.html', error="Falsches Passwort")  # Fehlermeldung bei falschem Passwort
        else:
            return render_template('Login.html', error="Benutzer nicht gefunden")  # Fehlermeldung bei Benutzer nicht gefunden
    
    return render_template('Login.html')

@app.route('/Registrieren', methods=['GET', 'POST'])
def Registrieren():
    if 'Angemeldet' in session:  # Wenn der Benutzer angemeldet ist
        return redirect(url_for('Home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('Nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('Registrieren.html', error="Benutzername existiert bereits.")
        
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('Login'))

    return render_template('Registrieren.html')

@app.route('/Abmelden')
def Abmelden():
    session.pop('Angemeldet', None)
    session.pop('username', None)
    return redirect(url_for('Home'))

# Diese Funktion stellt sicher, dass die geschützte Seite nur für eingeloggte Benutzer zugänglich ist
def Anmeldung_Benötigt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Angemeldet' not in session:
            return redirect(url_for('Home'))  # Wenn der Benutzer nicht eingeloggt ist, leite ihn zum Anmelden weiter
        return f(*args, **kwargs)
    return decorated_function

@app.route('/Gesichert')
@Anmeldung_Benötigt
def Gesichert():
    return f"Hallo {session.get('username')}, dies ist eine geschützte Seite."

@app.route('/Post')
def Post_Seite():
    if 'Angemeldet' in session:  # Benutzer ist angemeldet
        return render_template('Post.html', Angemeldet=True, username=session.get('username'))
    return render_template('Post.html', Angemeldet=False)  # Benutzer ist nicht angemeldet

@app.route('/Feed')
def Feed_Seite():
    if 'Angemeldet' in session:  # Benutzer ist angemeldet
        return render_template('Feed.html', Angemeldet=True, username=session.get('username'))
    return render_template('Feed.html', Angemeldet=False)  # Benutzer ist nicht angemeldet

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # Check if image file available
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        description = request.form.get('description')

        # if correct
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # save in feed
            new_post = Post(image_file=file.filename, description=description)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('feed'))  

    return render_template('post.html')  
if __name__ == "__main__":
    db.create_all()  
    app.run(debug=True)  

@app.route('/feed')
def feed():
    posts = Post.query.all()  # take all the available file
    return render_template('Feed.html', posts=posts)