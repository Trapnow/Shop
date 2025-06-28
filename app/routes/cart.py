from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user


from ..models.book import Cart, Book

from ..extensions import db

# Создаем blueprint для маршрутов корзины
cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def show_cart():
    cart_items = current_user.cart_items
    total = sum(item.book.price * item.quantity for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total)

@cart.route('/add_to_cart/<int:book_id>', methods=["POST"])
@login_required
def add_to_cart(book_id):
    existing_item = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    print(existing_item)

    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = Cart(user_id=current_user.id, book_id=book_id)
        db.session.add(new_item)

    db.session.commit()

    return redirect(url_for('book.list_books'))

@cart.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)

    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart.show_cart'))


@cart.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    action = request.args.get('action')
    cart_item = Cart.query.get_or_404(cart_id)

    if action == '+':
        cart_item.quantity += 1
    elif action == '-':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1

    db.session.commit()
    return redirect(url_for('cart.show_cart'))