from ..extensions import db
from datetime import datetime


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Section {self.title}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cart_items = db.relationship('Cart', backref='book', lazy=True)
    sales_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Book {self.title}"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Cart {self.user.email}"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='comments')
    book = db.relationship('Book', backref='comments')

    def __repr__(self):
        return f"<Comment {self.user.email}"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    delivery_method = db.Column(db.String(50), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Ожидает обработки')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_address = db.Column(db.String(255), nullable=True)
    pickup_point = db.Column(db.String(100), nullable=True)

    user = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Comment {self.user.email}"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    book = db.relationship('Book', backref='order_items')
