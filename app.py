from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

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
def home():
    return render_template('Hauptseite.html')

@app.route('/Post')
def Test_Seite():
    return render_template('Post.html')

@app.route('/Feed')
def Info_Seite():
    return render_template('Feed.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

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