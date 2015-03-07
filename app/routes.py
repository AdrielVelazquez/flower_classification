import os
from collections import defaultdict

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/imgs/temp"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

flower_dictionary = defaultdict(dict)

classification = Blueprint('classification', __name__, url_prefix='/classification',
                    template_folder='templates', static_folder='static')


@classification.route("/", methods=["GET", "POST"])
def default():
    return redirect(url_for("classification.main_application"))

@classification.route("/upload", methods=["POST", "GET"])
def main_application():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            return render_template("index.html", process="primary", file_path=file_path)
    return render_template("index.html", process="upload")
