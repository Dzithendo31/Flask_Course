from flask import request, render_template, Blueprint

main_bp = Blueprint('main_bp',__name__)

# Routes
@main_bp.route("/")  # HOF
def hello_world():
    return "<h1>Super, Cool 😁</h1>"
 
 
name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]
 
 
@main_bp.route("/profile")  # HOF
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)
  
# Task - Welcome message
@main_bp.route("/dashboard", methods=["POST"])  # HOF
def dashboard_page():
    username = request.form.get("username")  # request.form.get("key")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return "<h1>Dashboard page</h1>"