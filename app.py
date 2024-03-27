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
movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]
 
 
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
 
    # Creating the new id
    movie_ids = [int(movie["id"]) for movie in movies]
    max_id = max(movie_ids)
    new_movie["id"] = str(max_id + 1)
    # adding the to the list
    movies.append(new_movie)
 
    return "<h1>Movie added Successfully</h1>"
 
 
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