from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from ..functions import calculate_total_amount
from ..models.book import Order, OrderItem

from ..extensions import db

order = Blueprint('order', __name__)


@order.route('/order_form', methods=['GET', 'POST'])
@login_required
def order_form():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        delivery = request.form.get('delivery')
        delivery_date = request.form.get('delivery_date')
        delivery_address = request.form.get('address')
        pickup_point = request.form.get('pickup')
        total_amount = calculate_total_amount()

        cart_items = current_user.cart_items

        new_order = Order(
            user_id=current_user.id,
            name=name,
            phone=phone,
            delivery_method=delivery,
            delivery_date=datetime.strptime(delivery_date, '%Y-%m-%d'),
            total_amount=total_amount,
            delivery_address=delivery_address,  # сохраняем адрес
            pickup_point=pickup_point  # сохраняем пункт выдачи
        )

        db.session.add(new_order)

        for item in cart_items:
            order_item = OrderItem(
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price
            )
            new_order.order_items.append(order_item)

        db.session.commit()
        return redirect(url_for('cart.show_cart'))
    total_amount = calculate_total_amount()
    return render_template('order.html', total_amount=total_amount)


@order.route('/orders')
@login_required
def user_orders():
    orders = Order.query.filter_by(user_id=current_user.id) \
        .order_by(Order.created_at.desc()) \
        .all()
    return render_template('history_orders.html', orders=orders)


@order.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_details.html', order=order)


@order.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)

    order.status = 'Отменен'
    db.session.commit()

    return redirect(url_for('order.order_details', order_id=order_id))
