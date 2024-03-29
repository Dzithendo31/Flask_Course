from flask import Flask, jsonify,request,render_template
#Rewnder Template is inbulinf to Flas

app = Flask(__name__)

user = {
    'name':'Dhara',
    'pic': 'https://shiftart.com/wp-content/uploads/2017/04/RC-Profile-Square.jpg'
}
data_list = [
    {'name': 'Dhara', 'pic': 'https://shiftart.com/wp-content/uploads/2017/04/RC-Profile-Square.jpg'},
    {'name': 'John', 'pic': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MXw3NjA4Mjc3NHx8ZW58MHx8fHx8'},
    {'name': 'Emma', 'pic': 'https://profilemagazine.com/wp-content/uploads/2020/04/Ajmere-Dale-Square-thumbnail.jpg'}
]
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]
@app.route("/")
def hello_world():
    return "<p>Hddsddqq, 🥹</p>"

@app.route("/about")
def about_page():
    return render_template("about.html",people =data_list)


@app.route("/profile")
def profile_page():
    return render_template("profile.html",name=user["name"],hobbies = hobbies)

@app.route("/home")
def profile_page():
    return render_template("profile.html",name=user["name"],hobbies = hobbies)


@app.get('/movies')
def get_movies():
    #return movies #This is without conveetting to JSON
    return jsonify(movies)

#You want to do a bird
@app.post('/movies')
def post_movies():
    data = request.json #Get data from the JSON
    data['id'] = gethighestID(movies)
    movies.append(data)

    result = {
        'message' : 'Movie added successfully',
        'data': data
    }
    return jsonify(result),201

def gethighestID(movies):
    max_Id = max(movies,key=lambda x:int(x['id']))
    return str(int(max_Id['id'])+1)

#Get the actuall users using the ID
#http://127.0.0.1:5000/movies/99
@app.get('/movies/<id>')#Id is now a varibles
def get_movie(id):
    movie = next((movie for movie in movies if movie['id']==id),None)
    #movie = getMovieByID(id,movies)
    if movie == None:
        error = {'message':'Movie Not found'}
        return jsonify(error),404
    return jsonify(movie),200


@app.delete('/movies/<id>')
def delete_movie(id):
    movie_delete = next((movie for movie in movies if movie['id']==id),None)
    movie_delete = getMovieByID(id,movies)
    if movie_delete == None:
        error = {'message':'Movie Not found'}
        return jsonify(error),404
    movies.remove(movie_delete)
    return movie_delete
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # Permission to modify the lexical scope variable
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
 
#     if filtered_movie:
#         movies.remove(filtered_movie)
#         return jsonify({"message": "Deleted Successfully", "data": filtered_movie})
#     else:
#         return jsonify({"message": "Movie not found"}), 404

#Combination and Post I would say
@app.put('/movies/<id>')
def put_movie(id):
    data = request.json #Get data from the JSON
    #Get movie
    movie = next((movie for movie in movies if movie['id']==id),None)
    if movie:
        #movies.remove(movie)
        movie.update(data)
        #movies.append(movie)
        return jsonify({'message':'Movie Updated','data':movie}),200
    return jsonify({'message':'Movie Not found'}),404
# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}
def getMovieByID(id,movies):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return None


#To add the debug Flag
if __name__=="__main__":
    app.run(debug=True)




#List of dictionaries
#This data will be in our Database 
movies = [
  {
    "id": "99",
    "name": "Vikram",
    "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
    "rating": 8.4,
    "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
    "trailer": "https://www.youtube.com/embed/OKBMCL-frPU"
  },
  {
    "id": "100",
    "name": "RRR",
    "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
    "rating": 8.8,
    "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
    "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0"
  },
  {
    "id": "101",
    "name": "Iron man 2",
    "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
    "rating": 7,
    "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
    "trailer": "https://www.youtube.com/embed/wKtcmiifycU"
  },
  {
    "id": "102",
    "name": "No Country for Old Men",
    "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
    "rating": 8.1,
    "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
    "trailer": "https://www.youtube.com/embed/38A__WT3-o0"
  },
  {
    "id": "103",
    "name": "Jai Bhim",
    "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
    "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
    "rating": 8.8,
    "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA"
  },
  {
    "id": "104",
    "name": "The Avengers",
    "rating": 8,
    "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
    "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
    "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8"
  },
  {
    "id": "105",
    "name": "Interstellar",
    "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
    "rating": 8.6,
    "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
    "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E"
  },
  {
    "id": "106",
    "name": "Baahubali",
    "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
    "rating": 8,
    "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
    "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI"
  },
  {
    "id": "107",
    "name": "Ratatouille",
    "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
    "rating": 8,
    "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
    "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w"
  },
  {
    "name": "PS2",
    "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
    "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
    "rating": 8,
    "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
    "id": "108"
  },
  {
    "name": "Thor: Ragnarok",
    "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
    "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
    "rating": 8.8,
    "trailer": "https://youtu.be/NgsQ8mVkN8w",
    "id": "109"
  }
]
