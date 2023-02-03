from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.letter import Letter

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def home():
    return render_template("pages/home/home.html")


@dashboard.route('/dashboard')
@login_required
def statistics():
    letter_count = Letter.query.count()
    letter_done_count = Letter.query.filter(Letter.is_done.is_(True)).count()
    letter_not_done_count = Letter.query.filter(Letter.is_done.is_(False)).count()

    return render_template("pages/dashboard/statistics.html", user=current_user, stats={
        'letter_count': letter_count,
        'letter_done': letter_done_count,
        'letter_not_done': letter_not_done_count
    })
