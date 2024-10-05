import os
import pickledb
from flask import *

usersTable = pickledb.load(os.path.join("static", "Database", "users.db"), False)
usersTable.set('key', 'value')

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