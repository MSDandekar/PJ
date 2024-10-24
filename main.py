import os
import datetime
from flask import *
import mysql.connector

db = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "******",
	database = "PJ"
)
cursor = db.cursor(dictionary=True)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def sql_fetchAllUsers():
	sql = "SELECT * FROM Users WHERE userID != %s"
	cursor.execute(sql, (session['userID'], ))

	resultset = cursor.fetchall()

	return resultset

def sql_insertUsers(userName, userID, userEmail, userPassword):
	sql = "INSERT INTO Users (userName, userID, userEmail, userPassword) VALUES (%s, %s, %s, %s)"
	cursor.execute(sql, (userName, userID, userEmail, userPassword))
	db.commit()

def sql_fetchSpecificUser(userID):
	sql = "SELECT * FROM users WHERE UserID = %s"
	cursor.execute(sql, (userID, ))

	resultset = cursor.fetchone()

	return resultset

def sql_fetchFollowUsers(userID, mode):

	if mode == 0:
		sql = "SELECT * FROM Follow WHERE follower = %s"
	elif  mode == 1:
		sql = "SELECT * FROM Follow WHERE following = %s"

	cursor.execute(sql, (userID, ))

	resultset = cursor.fetchall()

	return resultset

def sql_fetchAllBlogs():
	sql = "SELECT * FROM Blogs"
	cursor.execute(sql)

	resultset = cursor.fetchall()

	return resultset

def sql_insertBlogs(blogTitle, blog):

	dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	sql = "INSERT INTO Blogs VALUES (%s, %s, %s, %s)"
	cursor.execute(sql, (session['userID'], dateTime, blogTitle, blog))
	db.commit()

def sql_followRequest(userID):
	sql = "INSERT INTO Follow VALUES (%s, %s)"
	cursor.execute(sql, (session['userID'], userID))
	db.commit()

@app.route("/")
def index():
	return render_template("Login.html")

@app.route("/signup")
def signup():
	return render_template("Signup.html")

@app.route("/profile")
def profile():
	if session.get("userID"):
		return render_template(
			"Profile.html", 
			profileData=sql_fetchSpecificUser(session['userID']), 
			following=len(sql_fetchFollowUsers(session['userID'], 0)), 
			followers=len(sql_fetchFollowUsers(session['userID'], 1))
		)
	return redirect(url_for("index"))

@app.route("/blogs")
def blogs():
	if session.get("userID"):
		return render_template(
			"Blogs.html", 
			blogs=sql_fetchAllBlogs()
		)

	return redirect(url_for("index"))

@app.route("/users")
def users():
	if session.get("userID"):
		return render_template(
			"Users.html", 
			users=sql_fetchAllUsers(), 
			dp=os.path.join("static", "DP")
		)

	return redirect(url_for("index"))

@app.route("/users/<userID>")
def user(userID):
	if session.get("userID"):
		if userID != session["userID"]:
			return render_template("User.html", user=sql_fetchSpecificUser(userID))
		else:
			return redirect(url_for("profile"))
	return redirect(url_for("index"))

@app.route("/b-signup", methods=["POST"])
def b_signup():
	if request.method == "POST":
		userName = request.form["userName"]
		userID = request.form["userID"]
		userEmail = request.form["userEmail"]
		userPassword = request.form["userPassword"]

		sql_insertUsers(userName, userID, userEmail, userPassword)
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

		resultset = sql_fetchSpecificUser(userID)

		print(resultset)

		if (userID == resultset["userID"]) and (userPassword == resultset["userPassword"]):
			
			session["userName"] = resultset["userName"]
			session["userID"] = resultset["userID"]
			session["userEmail"] = resultset["userEmail"]

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

		sql_insertBlogs(blogTitle, blog)

		return redirect(url_for("blogs"))

	return redirect(url_for("profile"))

@app.route("/b-follow/<userID>", methods=["POST"])
def b_follow(userID):
	if request.method == "POST":
		if session.get("userID"):
			sql_followRequest(userID)
		return redirect(url_for("users"))
	return redirect(url_for("index"))


if __name__ == "__main__":
	app.run(debug=True, port="4444")