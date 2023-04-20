from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5


# The rest of models.py looks like:
db = SQLAlchemy()

# as many of these as tables:

user_pokemon = db.Table("user_pokemon",
    db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    bio = db.Column(db.String, nullable = True)
    img_url = db.Column(db.String, nullable = True)
    pokemon = db.relationship('Pokemon', secondary=user_pokemon, backref=db.backref('users', lazy='select'))

    
    

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

    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)    
    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)

    def __init__(self, user_id, pokemon_id, name, hp, attack, defense, type, img_url, api_url):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.type = type
        self.img_url = img_url
        #thought maybe i need to call the api_url but still didnt work
        self.api_url = api_url
    
    def from_dict(self, data):
        self.user_id = data['user_id']
        self.pokemon_id = data['pokemon_id']
        self.name = data['name']
        self.hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.type = data['type']
        self.img_url = data['img_url']
    
    
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()



    
class MyPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    pokemon_obj = db.relationship('Pokemon', backref=db.backref('my_pokemon_list', lazy=True))

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

            



