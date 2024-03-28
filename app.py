import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from sqlalchemy import select
import uuid

#Imports for Forma and Form validations
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo,ValidationError

#Register the about_bp 
from about_bp import about_bp
#Register the movies_bp 
from movies_bp import movies_bp, Movie, db
#Register the movie_list dp
from movie_list_bp import movie_list_bp

load_dotenv()  # load -> os env (environmental variables)

 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FORM_SECRET_KEY")
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
    return render_template("login-form.html")
 
 
# Task - Welcome message
@app.route("/dashboard", methods=["POST"])  # HOF
def dashboard_page():
    username = request.form.get("username")  # request.form.get("key")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return "<h1>Dashboard page</h1>"
 

#Create a class from
#With Variables being the form feilds that we have

class RegistrationForm(FlaskForm):
    #Second Parameter is the type of Validations
    username = StringField('Username',validators=[InputRequired(),Length(min=3)])
    Realname = StringField('Realname',validators=[InputRequired(),Length(min=3)])
    #email = StringField('email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[
        InputRequired(), 
        Length(min=8,max=12),])
        #EqualTo('confirm_password', message='Passwords must match.')])
    #confirmPassword = PasswordField('Password',validators=[InputRequired(), Length(min=8,max=12)])

    #Finally we need the Submit Button
    submit = SubmitField("Sign up")

    #the method will automatically run when  form.validate_on_submit() is run
    def validate_username(self,field):
        print("Validate Username",field.data)
        if User.query.filter(User.username == field.data).first():
            raise ValidationError("Username is taken")

@app.route("/register", methods =["GET","POST"])  # HOF
def register_page():
    #Create a new ......?
    form = RegistrationForm()
    #So the method is bothe a get, and a post, only submit when its a post
    if form.validate_on_submit():
        print(form.username.data, form.password.data)
        new_user = User(
            username=form.username.data,
            real_name = form.Realname.data, 
            password=form.password.data
        )
        #try connect to database
        try:
          db.session.add(new_user)
          db.session.commit()
          # movies.append(new_movie)
          result = {"message": "Added successfully", "data": new_user.to_dict()}
          return "<h1>Successss</h1>"
        except Exception as e:
          db.session.rollback()  # Undo the change
          return f"<h1>Successss Not</h1>"
        #Now connect to the database
        
        
    #So in Get we get the Token and in Post we validate it.

    #This line wil run on get 
    return render_template("register.html", form =form)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True,default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100))
    real_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
 
    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
            "password": self.password
        }