from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5


# The rest of models.py looks like:
db = SQLAlchemy()

# as many of these as tables:


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    bio = db.Column(db.String, nullable = True)
    img_url = db.Column(db.String, nullable = True)
    
    

    def __init__(self, email, username, password, bio, img_url):
        self.email = email
        self.username = username
        self.password = password
        self.bio = bio
        self.img_url = img_url
        
    def from_dict(self, data):
        self.email=data['email']
        self.username=data['username']
        self.password=data['password']
        self.bio=data['bio']
        self.img_url = data['img_url']

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)    
    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
 
