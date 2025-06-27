from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"<User {self.name}"