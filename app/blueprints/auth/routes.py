from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.blueprints.auth import auth
from app.models import User

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')
        
        remember = True if request.form.get('remember_me') else False

        user = User.query.filter((User.username==username_or_email)|(User.email==username_or_email)).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash("Invalid username/email or password",'danger')
            
    return render_template('auth/login.html', title='Login')

@auth.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
              
        user_exists = User.query.filter((User.username==username)|(User.email==email)).first()
        if user_exists:
            flash("This user or email has already taken",'warning')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username,email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created successfully','success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', title = 'Register')

@auth.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out",'info')
    return redirect(url_for('auth.login'))
                  
            
    

        
    
        

            
        
    


