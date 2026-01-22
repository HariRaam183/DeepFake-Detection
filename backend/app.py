from flask import Flask, render_template, request, jsonify, send_from_directory
from predict import predict_image
from database import init_db, save_upload, get_all_uploads
import os

# Permanent paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

# Initialize DB
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# Serve uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Prediction API
@app.route("/predict_api", methods=["POST"])
def predict_api():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    result = predict_image(file_path)

    # Save in database
    save_upload(file.filename, result)

    return jsonify({"result": result})

# Admin dashboard
@app.route("/admin")
def admin():
    uploads = get_all_uploads()
    return render_template("admin.html", uploads=uploads)

if __name__ == "__main__":
    app.run(debug=True)
