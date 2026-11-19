import os
from flask_mail import Message
from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required, current_user
from app.models import Food,Cart,CartItem,Order,OrderItem
from app.utils import save_food_image
from unidecode import unidecode
from app.extensions import db, mail

main=Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    search_query= request.args.get('search_food','').strip()
    selected_category=request.args.get('category','').strip()
    
    query=Food.query
    
    if selected_category and selected_category != 'All':
        query=query.filter(Food.category==selected_category)   
        
    foods=query.all()
    
    if search_query:
        clean_search_query=unidecode(search_query).lower()
        keywords=clean_search_query.split()
        filtered_food=[]
        for food in foods:
            clean_food_name=unidecode(food.foodname).lower()
            match_all=True
            for word in keywords:
                if word not in clean_food_name:
                    match_all=False
                    break
                
            if match_all:
                filtered_food.append(food)
                
        foods=filtered_food
    
    categories=db.session.query(Food.category.distinct()).all()
    categories=[c[0] for c in categories if c[0]]
    
    return render_template('main/index.html', foods=foods, categories=categories,search_query=search_query, selected_category=selected_category)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@main.route('/food/<int:id>')
def food_detail(id):
    food=Food.query.get_or_404(id)
    return render_template('main/food_detail.html', food=food, title=food.foodname)
    
@main.route('/add-to-cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    cart=Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart=Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
        
    cart_item=CartItem.query.filter_by(cart_id=cart.id, food_id=id).first()
    
    if cart_item:
        cart_item.quantity +=1
    else:
        cart_item=CartItem(cart_id=cart.id, food_id=id, quantity=1)
        db.session.add(cart_item)
        
    db.session.commit()
    flash("Successfully added dish into cartt",'success')
    return redirect(url_for('main.cart'))
@main.route('/cart')
@login_required
def cart():
    cart=Cart.query.filter_by(user_id=current_user.id).first()
    cart_items=[]
    total_price=0
    
    if cart:
        for item in cart.items:
            subtotal=item.food.price * item.quantity
            total_price += subtotal
            cart_items.append({'food':item.food,'quantity':item.quantity,'subtotal':subtotal})
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@main.route('/remove-from-cart/<int:id>')
@login_required
def remove_from_cart(id):
    cart=Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_item=CartItem.query.filter_by(cart_id=cart.id, food_id=id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            flash("Deleted dish!",'info')
            
    return redirect((url_for('main.cart')))

@main.route('/checkout', methods=['GET','POST'])
@login_required
def check_out():
    cart=Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash("Your cart is empty!","warning")
        return redirect(url_for('main.index'))
        
    total_price=sum(item.food.price * item.quantity for item in cart.items)
    last_order=Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).first()
    
    if request.method=='POST':
        cus_name=request.form.get('cus_name')
        cus_email=request.form.get('cus_email')
        cus_phone=request.form.get('cus_phone')
        cus_address=request.form.get('cus_address')
        
        new_order=Order(
            user_id=current_user.id,
            total_price=total_price,
            cus_name=cus_name,
            cus_email=cus_email,
            cus_phone=cus_phone,
            cus_address=cus_address,
            status='Pending'  
        )
        db.session.add(new_order)
        db.session.commit()
        
        for cart_item in cart.items:
            order_item=OrderItem(
                order_id=new_order.id,
                food_id=cart_item.food_id,
                quantity=cart_item.quantity,
                price=cart_item.food.price
            )
            db.session.add(order_item)
        for cart_item in cart.items:
            db.session.delete(cart_item)
            
        db.session.commit()
        
        try:
            items_list="\n".join([
                f"- {item.food.foodname} x {item.quantity} : {item.price*item.quantity:,.0f}€"
                for item in new_order.items
            ])
            msg_admin= Message(
                subject=f"🔔 New order #{new_order.id} from Customer {new_order.user_id}",
                recipients=[os.environ.get('ADMIN_EMAIL')]
            )
            msg_admin.body= f"""You have received a new order!
OrderNr: #{new_order.id}
Customer: {new_order.user_id}
Phone: {new_order.cus_phone}
Delivery Address: {new_order.cus_address}

Order Details:
{items_list}

Total: {new_order.total_price:,.2f}€
Please visit the Admin Dashboard to process this order."""
            
            mail.send(msg_admin)
            
            if new_order.cus_email:
                msg_customer= Message(
                    subject=f"Order Confirmation - Oder #{new_order.id}",
                    recipients=[new_order.cus_email]
                )
                msg_customer.body= f"""
Thank you for your order! We have received your order and it is currently awaiting confirmation (Status: Pending).

ORDER SUMMARY: #{new_order.id}:
{items_list}

TOTAL PAID: {new_order.total_price:,.2f}€
Delivery Address: {new_order.cus_address}
Contact Phone:  {new_order.cus_phone}

We will send you another email as soon as your food is on the way!"""
                mail.send(msg_customer)
            
        except Exception as e:
            print(f"Error on sending email: {e}")
        
        flash("Order placed successfully!",'success')
        return redirect(url_for('main.my_orders'))
    
    return render_template('checkout.html', total_price=total_price, last_order=last_order)
@main.route('/my-orders')
@login_required
def my_orders():
    orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.create_at.desc()).all()
    return render_template('my_orders.html', orders=orders)
    
    