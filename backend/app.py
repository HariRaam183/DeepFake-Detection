from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
from predict import predict_image
from database import init_db, save_upload, get_all_uploads, register_user, login_user, get_user_by_id, get_user_uploads
import os

# Permanent paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.secret_key = "deepfake_secret_key_2026"  # Required for sessions

# Initialize DB
init_db()

# ========== AUTH ROUTES ==========

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        success, user = login_user(username, password)
        
        if success:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password!")
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match!")
        
        success, message = register_user(username, email, password)
        
        if success:
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error=message)
    
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ========== MAIN ROUTES ==========

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session.get("username"))

# Serve uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Prediction API
@app.route("/predict_api", methods=["POST"])
def predict_api():
    if "user_id" not in session:
        return jsonify({"error": "Please login first"}), 401
    
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    result = predict_image(file_path)

    # Save in database with user_id
    save_upload(file.filename, result, session.get("user_id"))

    return jsonify({"result": result})

# User's history
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    uploads = get_user_uploads(session["user_id"])
    return render_template("history.html", uploads=uploads, username=session.get("username"))

# Admin dashboard
@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    uploads = get_all_uploads()
    return render_template("admin.html", uploads=uploads)

if __name__ == "__main__":
    app.run(debug=True)
