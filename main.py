from flask import Flask
from config import Config
from models import db, UserModel
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


from auth import auth
import views

# blueprint for authentication routes
app.register_blueprint(auth, url_prefix="/auth")


