import os
from flask import Flask
from sqlalchemy.sql import text
from dotenv import load_dotenv

from models.user import User
#Register the about_bp 
from routes.about_bp import about_bp
#Register the movies_bp 
from routes.movies_bp import movies_bp
#Register the movie_list dp
from routes.movie_list_bp import movie_list_bp
#Register the UserBP 
from routes.user_bp import user_bp
#Register the UserBP 
from routes.main_bp import main_bp
load_dotenv()  # load -> os env (environmental variables)
from flask_login import LoginManager

#Import the DB
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FORM_SECRET_KEY")
# General pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>
#connection_string = os.environ.get("AZURE_DATABASE_URL")

#Connecting to Local
#PF35AXQW\SQLEXPRESS
# mssql+pyodbc://@<server_name>/<db_name>?driver=<driver_name>

connection_string = os.environ.get("LOCAL_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db.init_app(app)


login_manager = LoginManager()


login_manager.init_app(app)

app.register_blueprint(movies_bp, url_prefix = "/movies") 
app.register_blueprint(about_bp, url_prefix = "/about")
app.register_blueprint(movie_list_bp, url_prefix = "/movie-list") 
app.register_blueprint(user_bp) 
app.register_blueprint(main_bp, url_prefix = "/home")
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

 

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        #db.drop_all()
        #db.create_all()
except Exception as e:
    print("Error connecting to the database:", e)
 