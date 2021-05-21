from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Авторизуйтесь, чтобы попасть на эту страницу'

from app import routes, models
