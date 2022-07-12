from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "6153e8aa-01a3-4546-b8a0-e5bd57e272a4"

DATABASE = 'test_practice_db'

bcrypt = Bcrypt(app)