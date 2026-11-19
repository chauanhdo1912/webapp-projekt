# Entry point khởi động app
from app import create_app
from app.extensions import db
from app.models import User, Food, Cart, CartItem, Order, OrderItem

app = create_app()

with app.app_context():
    db.create_all()
    print("Updated Database")

if __name__=='__main__':
    app.run(debug=True)
    