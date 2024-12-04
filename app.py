import plotly.express as px
from flask import *
from flask_sqlalchemy import *
from flask_migrate import *
from flask_login import *
from flask_bcrypt import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'    
    
    login_manager = LoginManager()
    login_manager.init_app(app) 
    bcrypt = Bcrypt(app)
    migrate=Migrate(app,db)

    from models import Admin, Sponsor, Influencer, Ad, Campaign, Login
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(id):
        return Login.query.get(id)

        
    from routes import register_routes
    register_routes(app,db,bcrypt)

    
    return app