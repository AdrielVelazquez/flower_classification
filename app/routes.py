from flask import Blueprint, render_template, request

from app.views import *

classification = Blueprint('classification', __name__, url_prefix='/classification',
                    template_folder='templates', static_folder='static')

@classification.route("/")
def main_application():
    return render_template("index.html")