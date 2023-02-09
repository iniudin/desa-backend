from flask import Blueprint, render_template
from flask_login import current_user

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
    return render_template("pages/home/home.html", user=current_user)
