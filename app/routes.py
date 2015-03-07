import os
from collections import defaultdict

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/imgs/temp"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
image_size = (304, 228)

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
            img = Image.open(file_path)
            img.thumbnail(image_size, Image.ANTIALIAS)
            img.save(file_path)
            return render_template("index.html", process="primary", file_path=filename)
    return render_template("index.html", process="upload")


@classification.route("/get_coordinates_color", methods=["GET"])
def get_image():
    x = float(request.args.get("x"))
    y = float(request.args.get("y"))
    filename = request.args.get("filename").split("/")[-1]
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print file_path
    im = Image.open(file_path)
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((x, y))
    return jsonify({"RGB": (r, g, b)})
