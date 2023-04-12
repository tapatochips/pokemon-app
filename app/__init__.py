from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'pokemon'


from app import routes 

