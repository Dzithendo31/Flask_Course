from flask import Flask, jsonify, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models.movie import Movie, db


movie_list_bp = Blueprint('movie_list_bp',__name__)


#Here we are handing the actuall Action that hmovies_list_bpends in the thtml Forms
@movie_list_bp.route("/delete", methods=["POST"])  # HOF
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
@movie_list_bp.route("/")  # HOF
def movie_list_page():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return render_template("movie-list.html", movies=data)
 
 
# Task 3: /movies-list/99 -> Display the data on the page from Azure (MSSQL)
# Movie list detail
@movie_list_bp.route("/<id>")  # HOF
def movie_detail_page(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return render_template("movie-detail.html", movie=data)
    else:
        return "<h1>Movie not found</h1>"

@movie_list_bp.route("/add", methods=["GET"])  # HOF
def add_movie():
    return render_template("add-movie.html")
 
#I did the This by myslef 
@movie_list_bp.route("/success", methods=["POST"])  # HOF
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