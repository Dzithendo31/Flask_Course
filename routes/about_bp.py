from flask import Blueprint, render_template

#Now we have to declare it here in the file.
about_bp = Blueprint('about',__name__)


#Replace app with about_bp.route
@about_bp.route("/")  # HOF
def about_page():
    return render_template("about.html", users=users)

#The about Page using the ID per suer
#So this method uses The ID filetering.
@about_bp.route("/<id>")  # HOF
def about_page_Id(id):
    return render_template("about.html", users=[user for user in users if user['id']==id]) 


users = [
    {
        "id": "1",
        "name": "Dhara",
        "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Yolanda",
        "pic": "https://images.pexels.com/photos/3792581/pexels-photo-3792581.jpeg?cs=srgb&dl=pexels-matheus-bertelli-3792581.jpg&fm=jpg",
        "pro": False,
    },
    {
        "id": "3",
        "name": "Gemma",
        "pic": "https://wallpapers.com/images/hd/pretty-profile-pictures-2tkqwa8t2rolierf.jpg",
        "pro": True,
    },
]