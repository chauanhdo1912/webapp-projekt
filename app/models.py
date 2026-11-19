# Dinh nghia DB (User, Post)
from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(UserMixin,db.Model):
    
    __tablename__= "users"
    id=db.Column(db.Integer, primary_key = True)
    username=db.Column(db.String(64),unique=True,index=True,nullable=False)
    email=db.Column(db.String(120),unique=True,index=True,nullable=False)
    password_hash=db.Column(db.String(128),nullable=False)
    is_admin= db.Column(db.Boolean(), default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)   
@login_manager.user_loader 
def user_loader(user_id):
    return User.query.get(int(user_id))
    
class Food(db.Model):
    __tablename__="foods"
    id=db.Column(db.Integer, primary_key=True)
    foodname= db.Column(db.String(100),nullable=False)
    price=db.Column(db.Float,nullable=False) 
    description=db.Column(db.Text,nullable=True)
    image=db.Column(db.String(255),nullable=True, default='default.jpg')
    category=db.Column(db.String(50),nullable=True)
    
class Cart(db.Model):
    __tablename__="carts"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items=db.relationship('CartItem',backref='cart',cascade='all, delete-orphan')  
    
class CartItem(db.Model):
    __tablename__="cartItems"
    id=db.Column(db.Integer, primary_key=True)
    cart_id=db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    food_id=db.Column(db.Integer, db.ForeignKey('foods.id'),nullable=False)
    quantity=db.Column(db.Integer, default=1)
    
    food=db.relationship('Food')

class Order(db.Model):
    __tablename__='orders'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price=db.Column(db.Float, nullable=False)
    status=db.Column(db.String(50), default='Pending')
    create_at=db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    cus_name=db.Column(db.String(100), nullable=False)
    cus_email=db.Column(db.String(255), nullable=False)
    cus_phone=db.Column(db.String(20), nullable=False)
    cus_address=db.Column(db.String(255), nullable=False)
    
    items=db.relationship('OrderItem',backref='orders',lazy=True,cascade='all, delete-orphan')
    
class OrderItem(db.Model):
    __tablename__="orderItems"
    id=db.Column(db.Integer, primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_id=db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    price=db.Column(db.Float, nullable=False)
    
    food=db.relationship('Food', lazy=True)
    
    
    
    
    
    
    
    
    
    
# python -m flask db migrate -m "mo ta thay đổi của em (ví dụ: add user table)"
# flask db upgrade




