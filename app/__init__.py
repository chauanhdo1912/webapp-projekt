# Applcation Factoy 
# create_app()
import os
from dotenv import load_dotenv
from flask import Flask
from config import config
from app.extensions import db,migrate,login_manager, mail

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    #Configuration of Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
    
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from app.models import User, Food, Cart, CartItem, Order, OrderItem
    from app.blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
        
    from app.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.blueprints.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    return app
