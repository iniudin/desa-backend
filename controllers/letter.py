import os

from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

from app import db
from models.letter import Letter, File

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
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@letter.route("/letters")
def letter_list():
    data = Letter.query.all()
    return render_template("pages/letter/list.html", datas=data)


@letter.route("/letters/create", methods=["GET", "POST"])
def letter_create():
    if request.method == "POST":
        new_letter = Letter(
            nik=request.form.get('nik'),
            kk=request.form.get('kk'),
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            notes=request.form.get('notes'),
        )

        if 'fileKK' not in request.files:
            flash('Mohon upload foto / scan Kartu Keluarga!')
            return redirect(request.url)

        if 'fileKTP' not in request.files:
            flash('Mohon upload foto / scan Kartu Keluarga!')
            return redirect(request.url)

        for file in request.files.values():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                photo = File(url=filename, letter=new_letter)
                new_letter.files.append(photo)

        db.session.add(new_letter)
        db.session.commit()
        flash('Surat berhasil dikirim')
        return redirect(url_for("letters.letter_show", letter_id=new_letter.id))

    return render_template("pages/letter/create.html")


@letter.route("/letters/<int:letter_id>")
def letter_show(letter_id):
    data = db.get_or_404(Letter, letter_id)
    return render_template("pages/letter/show.html", data=data)


@letter.route("/letters/<int:letter_id>/update")
def letter_update(letter_id):
    data = db.get_or_404(Letter, letter_id)
    return render_template("pages/letter/detail.html", letter=data)


@letter.route("/letters/<int:letter_id>/delete", methods=["GET"])
def letter_delete(letter_id):
    data = db.get_or_404(Letter, letter_id)
    db.session.delete(data)
    db.session.commit()

    return render_template("pages/letter/delete.html", letter=data)
