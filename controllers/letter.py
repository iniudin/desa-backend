import os

from flask import Blueprint, render_template, send_from_directory, url_for, redirect, flash
from flask_login import login_required, current_user

from app import db
from models.letter import Letter

letter = Blueprint('letters', __name__)

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'files')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@letter.route('/uploads/<name>')
@login_required
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@letter.route("/letters/<int:letter_id>")
@login_required
def letter_show(letter_id):
    data = db.get_or_404(Letter, letter_id)
    return render_template("pages/letter/show.html", data=data, user=current_user)


@letter.route("/letters/<int:letter_id>/update")
@login_required
def letter_update(letter_id):
    data = Letter.query.filter_by(id=letter_id).first()
    data.is_done = True
    db.session.commit()

    flash('Berhasil mengubah status surat', "success")
    return redirect(url_for('dashboard.statistics'))


@letter.route("/letters/<int:letter_id>/delete", methods=["GET"])
@login_required
def letter_delete(letter_id):
    data = Letter.query.filter_by(id=letter_id).first()
    for img in data.files:
        filepath = os.path.join(UPLOAD_FOLDER, img.url)
        os.remove(filepath)

    db.session.delete(data)
    db.session.commit()
    flash('Surat berhasil dihapus.', "success")

    return redirect(url_for('dashboard.statistics'))
