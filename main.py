import os
import json
from flask import *
from tinydb import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = TinyDB(os.path.join("static", "Database", "db.json"))
query = Query()
usersTable = db.table("Users")

@app.route("/")
def index():
	return render_template("Index.html")

@app.route("/login")
def login():
	return render_template("Login.html")

@app.route("/signup")
def signup():
	return render_template("Signup.html")

@app.route("/profile")
def profile():
	if session.get("userID"):
		return render_template("Profile.html", profileData=[session["userName"], session["userID"], session["userEmail"]])
	return redirect("index")

@app.route("/b-signup", methods=["POST"])
def b_signup():
	if request.method == "POST":
		userName = request.form["userName"]
		userID = request.form["userID"]
		userEmail = request.form["userEmail"]
		userPassword = request.form["userPassword"]

		usersTable.insert({"userName": userName, "userID": userID, "userEmail": userEmail, "userPassword": userPassword})
	else:
		print("Signup ERROR!")
	return redirect(url_for("index"))

@app.route("/b-login", methods=["POST"])
def b_login():
	if request.method == "POST":
		userID = request.form["userID"]
		userPassword = request.form["userPassword"]

		userData = usersTable.search(query.userID == userID) and usersTable.search(query.userPassword == userPassword)

		if len(userData) > 0:
			
			session["userName"] = userData[0]["userName"]
			session["userID"] = userData[0]["userID"]
			session["userEmail"] = userData[0]["userEmail"]

			return redirect(url_for("profile"))
		else:
			print("Incorrect Info!")
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(debug=True, port="4444")