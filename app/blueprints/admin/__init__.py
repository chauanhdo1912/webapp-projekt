from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from flask_mail import Message
from functools import wraps
from app.extensions import db, mail
from app.models import User, Order, Food
from app.utils import save_food_image

admin=Blueprint('admin',__name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or not current_user.is_admin:
            flash("Access denied! Admin privileges required.", 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
@admin.route('/add_food', methods=['GET','POST'])
@login_required
@admin_required
def add_food():
    
    if request.method == 'POST':
        foodname=request.form.get('foodname')
        price=request.form.get('price')
        description=request.form.get('description')
        category=request.form.get('catefory')
        image=request.files.get('image')
        new_image=save_food_image(image)
        if new_image:
            image=new_image
        new_food=Food(
            foodname=foodname,
            price=price,
            description=description,
            category=category,
            image=image
        )
        db.session.add(new_food)
        db.session.commit()  
        flash("Added food successfully", 'success') 
        return redirect(url_for('main.index'))
            
    return render_template('admin/add_food.html')

@admin.route('/delete_food/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_food(id):
    food=Food.query.get_or_404(id)
    
    db.session.delete(food)
    db.session.commit()
    
    flash("Successfully deleted",'success')
    return redirect(url_for('main.index'))

@admin.route('/edit_food/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_food(id):
    food=Food.query.get_or_404(id)
    
    if request.method=='POST':
        food.foodname=request.form.get('foodname')
        price_val=request.form.get('price')
        food.price=float(price_val) if price_val else 0.0
        food.category=request.form.get('category')
        food.description=request.form.get('description')
        image_file = request.files.get('image')
        new_image=save_food_image(image_file)
        if new_image:
            food.image=new_image
            
        db.session.commit()
        flash("Already updated new fooddata")
        return redirect(url_for('main.index'))
    
    return render_template('admin/edit_food.html',food=food,title="Edit Food")            

    
# Route Order Dashboard
@admin.route('/admin_orders')
@login_required
@admin_required
def admin_orders():
    status_filter=request.args.get('status','All')
    query=Order.query.order_by(Order.id.desc())
    if status_filter in ['Pending','Shipping','Completed']:
        filtered_orders=query.filter_by(status=status_filter).all()
    else:
        status_filter='All'
        filtered_orders=query.all()
        
    all_orders= Order.query.all()
    total_revenue=sum(o.total_price for o in all_orders if o.status=='Completed')
    pending_count=sum(1 for o in all_orders if o.status=='Pending')
    shipping_count=sum(1 for o in all_orders if o.status=='Shipping')
    completed_count=sum(1 for o in all_orders if o.status=='Completed')
    
    return render_template('admin/orders.html', orders=filtered_orders, current_filter=status_filter, total_revenue=total_revenue, pending_count=pending_count, shipping_count=shipping_count, completed_count=completed_count)
# Route orders status update
@admin.route('/order/<int:order_id>/update', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order=Order.query.get_or_404(order_id)
    new_status=request.form.get('status')
    
    if new_status in ['Pending','Shipping','Completed']:
        order.status=new_status
        db.session.commit()
        
        if order.cus_email:
            try:
                status_msg={
                    'Pending':'Your order has been received and is pending confirmation.',
                    'Shipping':'Your order is freshly prepared and currently on its way to you!',
                    'Completed':'Your order has been delivered. Enjoy your meal!'
                }
                msg=Message(
                    subject=f" Order #{order_id} Status Update: {new_status}",
                    recipients=[order.cus_email]
                )
                msg.body=f"""Hello {order.cus_name},
The status of your order #{order_id} has been updated to: {new_status.upper()}
{status_msg.get(new_status,'')}

Total Amount: {order.total_price:,.2f}€
Delivery Address: {order.cus_address}"""
                mail.send(msg)
            except Exception as e:
                print(f"Customer email error: {e}")
                
        flash(f"Order #{order.id} status updated to {new_status}!",'success')
    else:
        flash("Invalid order status.",'success')
                
    
    return redirect(url_for('admin.admin_orders'))

