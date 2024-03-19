from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hddsddqq, 🥹</p>"

@app.route("/about")
def about_page():
    return "<h1>About Page</h1>"

#To add the debug Flag
if __name__=="__main__":
    app.run(debug=True)