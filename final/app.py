import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required, apology

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Session(app)

db = SQL("sqlite:///study_notes.db")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    summaries = db.execute("SELECT summaries.id, title, subject, year, username FROM summaries JOIN users ON summaries.user_id = users.id ORDER BY summaries.id DESC")
    return render_template("index.html", summaries=summaries)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must provide username and password")
        if password != confirmation:
            return apology("passwords must match")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username exists")
        hash = generate_password_hash(password)
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("must provide username and password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username/password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form.get("title")
        subject = request.form.get("subject")
        year = request.form.get("year")
        file = request.files["file"]

        if not title or not subject or not year or not file:
            return apology("all fields required")
        if not allowed_file(file.filename):
            return apology("only PDF files allowed")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        db.execute("INSERT INTO summaries (user_id, title, subject, year, filename) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], title, subject, year, filename)
        return redirect("/")

    return render_template("upload.html")


@app.route("/summary/<int:id>")
def summary(id):
    summary = db.execute("SELECT summaries.*, username FROM summaries JOIN users ON summaries.user_id = users.id WHERE summaries.id = ?", id)
    if not summary:
        return apology("summary not found")
    return render_template("summary.html", summary=summary[0])


@app.route("/profile/<int:user_id>")
def profile(user_id):
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if not user:
        return apology("user not found")
    summaries = db.execute("SELECT * FROM summaries WHERE user_id = ?", user_id)
    return render_template("profile.html", user=user[0], summaries=summaries)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return redirect("/")
    summaries = db.execute("SELECT summaries.id, title, subject, year, username FROM summaries JOIN users ON summaries.user_id = users.id WHERE title LIKE ? OR subject LIKE ? ORDER BY summaries.id DESC",
                           f"%{query}%", f"%{query}%")
    return render_template("search.html", summaries=summaries, query=query)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


url(C:\Users\workstation\Videos\Captures\app.py - final - Visual Studio Code 2025-08-23 07-26-56.mp4)