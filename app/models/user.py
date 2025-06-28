from ..extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    avatar = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(200))
    cart_items = db.relationship('Cart', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}"