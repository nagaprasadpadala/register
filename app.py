from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key for session
app.secret_key = "my-secret-key-123"


# -----------------------------
# MySQL Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="login_app"
    )


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("signin"))


# -----------------------------
# Signup Page
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        # Basic validation
        if not name or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("signup"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("signup"))

        try:

            db = get_db_connection()
            cursor = db.cursor()

            # Check if email already exists
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                db.close()

                flash("Email already registered.")
                return redirect(url_for("signup"))

            # Hash password
            hashed_password = generate_password_hash(password)

            # Insert user
            cursor.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            db.commit()

            cursor.close()
            db.close()

            flash("Account created successfully. Please sign in.")

            return redirect(url_for("signin"))

        except mysql.connector.Error as error:

            print("Database error:", error)

            flash("Something went wrong. Please try again.")

            return redirect(url_for("signup"))

    return render_template("signup.html")


# -----------------------------
# Signin Page
# -----------------------------
@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("signin"))

        try:

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )

            user = cursor.fetchone()

            cursor.close()
            db.close()

            # Check user
            if user and check_password_hash(
                user["password"],
                password
            ):

                # Store user information in session
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]

                return redirect(url_for("dashboard"))

            else:

                flash("Invalid email or password.")

                return redirect(url_for("signin"))

        except mysql.connector.Error as error:

            print("Database error:", error)

            flash("Something went wrong. Please try again.")

            return redirect(url_for("signin"))

    return render_template("signin.html")


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("signin"))

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        email=session["user_email"]
    )


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("signin"))


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)