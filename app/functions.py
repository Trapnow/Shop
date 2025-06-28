import secrets
import os.path

from  PIL import Image

from .extensions import db

from flask import current_app
from flask_login import current_user


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def calculate_average_rating(book):
    ratings = [comment.rating for comment in book.comments if comment.rating is not None]

    if ratings:
        total_rating = sum(ratings)
        count = len(ratings)
        book.rating = round(total_rating / count, 2)
    else:
        book.rating = 0

    db.session.commit()

def calculate_total_amount():
    # Здесь логика расчета общей суммы заказа
    # Например:
    cart_items = current_user.cart_items
    total = sum(item.book.price * item.quantity for item in cart_items)
    return total