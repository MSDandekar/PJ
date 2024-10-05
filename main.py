import os
from flask import *

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("Index.html")

@app.route("/login")
def login():
	return render_template("Login.html")

@app.route("/signup")
def signup():
	return render_template("Signup.html")

if __name__ == "__main__":
	app.run(debug=True, port="4444")