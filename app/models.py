from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# The rest of models.py looks like:
db = SQLAlchemy()

# as many of these as tables:


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
 
