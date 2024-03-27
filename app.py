import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid

#Register the about_bp 
from about_bp import about_bp
#Register the movies_bp 
from movies_bp import movies_bp, Movie, db
#Register the movie_list dp
from movie_list_bp import movie_list_bp

load_dotenv()  # load -> os env (environmental variables)
print(os.environ.get("AZURE_DATABASE_URL"))
 
app = Flask(__name__)
# General pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db.init_app(app)
 
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)
 
app.register_blueprint(movies_bp, url_prefix = "/movies") 
app.register_blueprint(about_bp, url_prefix = "/about")
app.register_blueprint(movie_list_bp, url_prefix = "/movie-list") 
 
# Routes
@app.route("/")  # HOF
def hello_world():
    return "<h1>Super, Cool 😁</h1>"
 
 
name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]
 
 
@app.route("/profile")  # HOF
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)
 
 
@app.route("/login", methods=["GET"])  # HOF
def login_page():
    return render_template("forms.html")
 
 
# Task - Welcome message
@app.route("/dashboard", methods=["POST"])  # HOF
def dashboard_page():
    username = request.form.get("username")  # request.form.get("key")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return "<h1>Dashboard page</h1>"
 


