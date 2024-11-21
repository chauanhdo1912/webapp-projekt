from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Hauptseite.html')

@app.route('/Testseite')
def Test_Seite():
    return render_template('Testseite.html')

@app.route('/Infoseite')
def Info_Seite():
    return render_template('Infoseite.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

if __name__ == "__main__":
    app.run(debug=True)