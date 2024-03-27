import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid
 
load_dotenv()  # load -> os env (environmental variables)
print(os.environ.get("AZURE_DATABASE_URL"))
 
app = Flask(__name__)
# General pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)  # ORM
 
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)
 
 
# Model (SQLAlchemy) == Schema
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True,default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))
 
    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }
 
 
# local
# /dashboard

# GET -> /movies -> JSON
@app.get("/movies")
def get_movies():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return jsonify(data)
 
 
# Task 1: Data from Azure (MSSQL)
# Clue: .all() - .get()
@app.get("/movies/<id>")
def get_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return jsonify(data)
    else:
        return jsonify({"message": "Movie not found"}), 404
 
 
# Task 4 | db.session.delete(movie)
@app.delete('/movies/<id>')
def delete_movie(id):
    movie_delete = Movie.query.get(id)
    if not movie_delete:
        #Catch the client Side error
        error = {'message':'Movie Not found'}
        return jsonify(error),404
    try:
        data = movie_delete.to_dict()
        db.session.delete(movie_delete)

        #Then you commit
        db.session.commit()
        return jsonify({"message": "Deleted Successfully", "data": data})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


#Here we are handing the actuall Action that happends in the thtml Forms
@app.route("/movie-list/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    print(request.form.get("movie_id"))
    movie_id = request.form.get("movie_id")
    filter_movie = Movie.query.get(movie_id)
    if not filter_movie:
        return "<h1>Movie not Found</h1>"
    try:
        data = filter_movie.to_dict()
        db.session.delete(filter_movie)
        db.session.commit()
        return f"<h1>{data['name']} deleted Successfully</h1>"        
    except Exception as e:
        db.session.rollback()
        return f"<h1>Movie Deletion Failed {str(e)}</h1>"

 
# Task 2: /movies-list -> Display the data on the page from Azure (MSSQL)
# Movie list dashboard
@app.route("/movie-list")  # HOF
def movie_list_page():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return render_template("movie-list.html", movies=data)
 
 
# Task 3: /movies-list/99 -> Display the data on the page from Azure (MSSQL)
# Movie list detail
@app.route("/movie-list/<id>")  # HOF
def movie_detail_page(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return render_template("movie-detail.html", movie=data)
    else:
        return "<h1>Movie not found</h1>"
 
 
# jinja2 - templates
 
users = [
    {
        "name": "Dhara",
        "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": True,
    },
    {
        "name": "Yolanda",
        "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": False,
    },
    {
        "name": "Gemma",
        "pic": "https://newprofilepic.photo-cdn.net//assets/images/article/profile.jpg?90af0c8",
        "pro": True,
    },
]
 
 
@app.route("/")  # HOF
def hello_world():
    return "<h1>Super, Cool 😁</h1>"
 
 
name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]
 
 
@app.route("/profile")  # HOF
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)
 
 
@app.route("/about")  # HOF
def about_page():
    return render_template("about.html", users=users)
 
 
@app.route("/movie-list/add", methods=["GET"])  # HOF
def add_movie():
    return render_template("add-movie.html")
 
#I did the This by myslef 
@app.route("/movie-list/success", methods=["POST"])  # HOF
def create_movie():
    name = request.form.get("name")
    poster = request.form.get("poster")
    rating = request.form.get("rating")
    summary = request.form.get("summary")
    trailer = request.form.get("trailer")
    print(name, poster, rating, summary, trailer)
 
    # Creating a dictionary
    new_movie = {
        "name": name,
        "poster": poster,
        "rating": rating,
        "summary": summary,
        "trailer": trailer,
    }
    new_movie = Movie(**new_movie)
    try:
        
    # Creating the new id

    # adding the to the list
      db.session.add(new_movie)
      db.session.commit()
      return "<h1>Movie added Successfully</h1>"
    except Exception as e:
        db.session.rollback()
        return f"<h1>Error adding Movie: {str(e)}</h1>"
 
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
 
 
# Not secure | Eg - Search functionality
# @app.route("/dashboard", methods=["GET"])  # HOF
# def dashboard_page():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     print("Dashboard page", username, password)
#     return "<h1>Dashboard page</h1>"
 
 
# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list
# 5 fields
# {
#         "name": "Vikram",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
#         "rating": 8.4,
#         "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
#         "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
# }
 
 
# Task
# Goto -> http://127.0.0.1:5000/movie-list/100 -> Detail of that particular movie alone
 
 
@app.put("/movies/<id>")
def update_movie_by_id(id):
    filtered_movie = next(
        (movie for movie in movies if movie["id"] == id), None
    )  # same memory
    body = request.json
 
    if filtered_movie:
        filtered_movie.update(body)  # same memory | mutable
        return jsonify({"message": "Updated Successfully", "data": filtered_movie})
    else:
        return jsonify({"message": "Movie not found"}), 404
 
 
@app.post("/movies")
def create_movies():
    new_movie = request.json
    # start
    movie_ids = [int(movie["id"]) for movie in movies]
    max_id = max(movie_ids)
    new_movie["id"] = str(max_id + 1)
    # end
    movies.append(new_movie)
    result = {"message": "Added successfully", "data": new_movie}
    return jsonify(result), 201



