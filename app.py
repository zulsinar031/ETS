from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import json

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ets_db"

app.secret_key = "xyz"

mysql = MySQL(app)


def check_user_exists(cursor, username):
    cursor.execute("""SELECT * FROM user WHERE user_name = %s""", ([username]))
    if cursor.fetchone() is None:
        return False
    else:
        return True


@app.route("/ets_home")
def home():
    if session.get("token"):
        return render_template("ets_home.html", username=session["username"])
    else:
        return redirect(url_for("ets_login"))


@app.route("/ets_login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # user_id = uuid4()
        username = json.loads(request.data)["username"]
        password = json.loads(request.data)["password"]
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Check if user exists
        cur = mysql.connection.cursor()
        # if check_user_exists(cur, username):
        #    return jsonify({"status": "failed", "message": "User already exists."})

        cur.execute(
            """SELECT * FROM user WHERE user_name=%s AND user_password=%s""",
            ([username], [password]),
        )
        mysql.connection.commit()
        user = cur.fetchone()
        cur.close()
        if user:
            # session["token"] = username
            session["token"] = user[0]
            session["username"] = user[1]
            return jsonify({"status": "success", "message": "Succesfully log in"})
        else:
            return jsonify({"Credentials incorrect"})
    else:
        is_login = False
        if session.get("token"):
            is_login = True
        return render_template("ets_login.html", is_login=is_login)


@app.route("/logout")
def logout():
    #session.pop("loggedin", None)
    #session.pop("user_id", None)
    #session.pop("user_email", None)
    session.clear()
    return redirect(url_for("ets_login"))


@app.route("/ets_register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # user_id = uuid4()
        username = json.loads(request.data)["username"]
        email = json.loads(request.data)["email"]
        password = json.loads(request.data)["password"]
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Check if user exists
        cur = mysql.connection.cursor()
        if check_user_exists(cur, username):
            return jsonify({"status": "failed", "message": "User already exists."})

        cur.execute(
            """INSERT INTO user (user_name, user_email, user_password) VALUES (%s, %s, %s)""",
            ([username], [email], [password]),
        )
        mysql.connection.commit()
        cur.close()

        # Success
        return jsonify({"status": "success", "message": "Registration successful."})
    else:
        is_login = False
        if session.get("token"):
            is_login = True
        return render_template("ets_register.html", is_login=is_login)


if __name__ == "__main__":
    app.run(debug=True)
