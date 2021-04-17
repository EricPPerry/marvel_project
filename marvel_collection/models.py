from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(100), nullable = True, default = '')
    last_name = db.Column(db.String(100), nullable = True, default = '')
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)
    ######
    about_me = db.Column(db.String(140))
    #last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable = True, default = '')

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', username = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.username = username



    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hashed = generate_password_hash(password)
        return self.pw_hashed

    def __repr__(self):
        return f'Welcome! User {self.email} has been created and you may now start your collection!'

class Character(db.Model):
    id = db.Column(db.String, primary_key=True)
    character_name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    #comics_appeared_in = db.Column(db.String(150))


    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, character_name, description, comics_appeared_in, super_power, user_token, id=''):
        self.id = self.set_id()
        self.character_name = character_name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token

    def __repr__(self):
        return f'The following character has been added: {self.character_name}'

    def set_id(self):
        return secrets.token_urlsafe()


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'character_name', 'description', 'comics_appeared_in', 'super_power']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)
    