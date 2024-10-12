import os
import datetime
from flask import *
from tinydb import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = TinyDB(os.path.join("static", "Database", "db.json"))
cursor = Query()

usersTable = db.table("Users")
blogsTable = db.table("Blogs")

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
		return render_template("Profile.html", profileData={"userName": session["userName"], "userID": session["userID"], "userEmail": session["userEmail"]})
	return redirect(url_for("index"))

@app.route("/blogs")
def blogs():
	if session.get("userID"):
		return render_template("Blogs.html", blogs=blogsTable.all())
	return redirect(url_for("index"))

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

		print(userID)
		print(userPassword)

		userData = usersTable.search((cursor.userID == userID) & (cursor.userPassword == userPassword))

		print(userData)

		if len(userData) > 0:
			
			session["userName"] = userData[0]["userName"]
			session["userID"] = userData[0]["userID"]
			session["userEmail"] = userData[0]["userEmail"]

			return redirect(url_for("profile"))
		else:
			print("Incorrect Info!")
	return redirect(url_for("index"))

@app.route("/b-logout", methods=["POST"])
def b_logout():
	if request.method == "POST":
		session.pop("userName", None)
		session.pop("userID", None)
		session.pop("userEmail", None)
	return redirect(url_for("index"))

@app.route("/b-blog", methods=["POST"])
def b_blog():
	if request.method == "POST":
		blogTitle = request.form["blogTitle"]
		blog = request.form["blog"]

		blogsTable.insert({"userID": session["userID"], "dateTime": str(datetime.datetime.now()), "blogTitle": blogTitle, "blog": blog})

		return redirect(url_for("blogs"))

	return redirect(url_for("profile"))

if __name__ == "__main__":
	app.run(debug=True, port="4444")