import os
from collections import defaultdict
import csv

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/imgs/temp"
CSV_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/csv/master.csv"
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
    process = request.args.get("process")
    if process == "submit":
        submit()
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
    process = request.args.get("process")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    im = Image.open(file_path)
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((x, y))
    flower_dictionary[filename]["{}_RGB".format(process)] = (r, g, b)
    print flower_dictionary
    return jsonify({"RGB": (r, g, b)})


@classification.route("/counter", methods=["GET"])
def save_count():
    filename = request.args.get("filename").split("/")[-1]
    count = int(request.args.get("count"))
    flower_dictionary[filename]["count"] = count
    return jsonify({"RGB": 0})

@classification.route("/picker", methods=["GET"])
def second_image():
    filename = request.args.get("filename")
    process = request.args.get("process")
    return render_template("index.html", process=process, file_path=filename)

@classification.route("/count", methods=["GET"])
def petal_count():
    filename = request.args.get("filename")
    process = request.args.get("process")
    return render_template("index.html", process=process, file_path=filename)

@classification.route("/stem_color", methods=["GET"])
def stem_color():
    filename = request.args.get("filename")
    process = request.args.get("process")
    return render_template("index.html", process=process, file_path=filename)


def submit():
    filename = request.args.get("filename").split("/")[-1]
    flower_dict = flower_dictionary[filename]
    line = [filename]
    keys = ['count','stem_color_RGB','primary_RGB','secondary_RGB']
    line.extend([flower_dict.get(key) for key in keys])
    writer = csv.writer(open(CSV_FOLDER, 'a'))
    writer.writerow(line)
