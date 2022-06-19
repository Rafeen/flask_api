from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=True)
    nickname = db.Column(db.String(), nullable=True, default="")
    comment = db.Column(db.String(), nullable=True, default="")

    def __init__(self, user_id):
        self.user_id = user_id
        self.nickname = user_id

    def serialize(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'comment': self.comment,
        }


    def __repr__(self):
        return f"{self.nickname}:{self.user_id}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
