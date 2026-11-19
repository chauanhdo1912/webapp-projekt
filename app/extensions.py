# Khai bao tien ich doc lap (db, migrate, login_manager)
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail=Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///dev.db")