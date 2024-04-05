from flask import render_template, Blueprint, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import flask
from flask_login import login_required, login_user, logout_user
from models.user import User, db
#Imports for Forma and Form validations
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo,ValidationError

user_bp = Blueprint('user_bp',__name__)

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

@user_bp.route("/register", methods =["GET","POST"])  # HOF
def register_page():
    #Create a new ......?
    form = RegistrationForm()
    #So the method is bothe a get, and a post, only submit when its a post
    if form.validate_on_submit():
        print(form.username.data, form.password.data)
        #But this will Require space
        password_hash = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            real_name = form.Realname.data,
            #This is where the hashPassword Occurs 
            password=password_hash
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
    return render_template("register.html", form =form)



# LogIn details
class LoginForm(FlaskForm):
    #Second Parameter is the type of Validations
    username = StringField('Username',validators=[InputRequired(),Length(min=3)])
    Realname = StringField('Realname',validators=[InputRequired(),Length(min=3)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=12),])
    submit = SubmitField("Log In")

    #the method will automatically run when  form.validate_on_submit() is run
    def validate_username(self,field):
        user_from_db = User.query.filter(User.username == field.data).first()
        if not user_from_db:
            raise ValidationError("Invalid Credentitals")
        
    def validate_password(self,field):
        user_from_db = User.query.filter(User.username == field.data).first()
        if user_from_db:
          user_db_data = user_from_db.to_dict()
          formPassowrd = field.data
          print(user_db_data, formPassowrd)
          if not check_password_hash(user_db_data['password'],formPassowrd):
              raise ValidationError("Invalid Credentials")




@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)#Token is Stored in the browser.
            flask.flash('Logged in successfully.')
            # Redirect to the next page if available, otherwise to the home page
            next_page = flask.request.args.get('next') or url_for('movie_list_bp.movie_list_page')
            return redirect(next_page)
        else:
            flask.flash('Invalid username or password.', 'error')
    return render_template("login-form.html", form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')