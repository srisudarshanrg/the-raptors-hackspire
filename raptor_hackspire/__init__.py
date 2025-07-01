from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import session
from flask_login import current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///raptors_hackspire.db"
app.config["SECRET_KEY"] = "b17540d9a1a7e54eedf84gf6"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_branch"    
login_manager.login_message = "Login is required to access this page or feature"
login_manager.login_message_category = "info"

session = session

bcrypt = Bcrypt(app)

from . import routes