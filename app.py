from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))  # Thư mục gốc của ứng dụng
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
        # Kiểm tra nếu có file ảnh
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        description = request.form.get('description')

        # Nếu file hợp lệ, lưu file và mô tả vào cơ sở dữ liệu
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Lưu vào cơ sở dữ liệu
            new_post = Post(image_file=file.filename, description=description)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('feed'))  # Sau khi đăng, chuyển hướng đến trang feed

    return render_template('post.html')  # Hiển thị trang post khi phương thức GET

if __name__ == "__main__":
    db.create_all()  # Tạo cơ sở dữ liệu nếu chưa tồn tại
    app.run(debug=True)  # Chạy Fl

@app.route('/feed')
def feed():
    posts = Post.query.all()  # Lấy tất cả bài đăng từ cơ sở dữ liệu
    return render_template('Feed.html', posts=posts)