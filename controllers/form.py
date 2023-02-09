import datetime
import os
import uuid

from flask import Blueprint, request, redirect, render_template, flash
from flask_login import current_user

from app.database import db
from models.letter import Letter, File

forms = Blueprint('forms', __name__)
# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'files')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@forms.route("/surat-keterangan", methods=["GET", "POST"])
def surat_keterangan():
    if request.method == "POST":
        new_letter = Letter(
            nik=request.form.get('nik'),
            kk=request.form.get('kk'),
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            notes=request.form.get('notes'),
            type="keterangan",
            created_at=datetime.datetime.now()
        )

        if 'fileKK' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        if 'fileKTP' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        for file in request.files.values():
            content_type = file.filename.split(".")[1]
            filename = f"{str(uuid.uuid4())}.{content_type}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            photo = File(url=filename, letter=new_letter)
            new_letter.files.append(photo)

        db.session.add(new_letter)
        db.session.commit()
        flash('Surat berhasil dikirim', 'success')
        return render_template("pages/letter/surat-ketarangan.html", user=current_user)

    return render_template("pages/letter/surat-ketarangan.html", user=current_user)


@forms.route("/surat-pernyataan", methods=["GET", "POST"])
def surat_pernyataan():
    if request.method == "POST":
        new_letter = Letter(
            nik=request.form.get('nik'),
            kk=request.form.get('kk'),
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            notes=request.form.get('notes'),
            type="pernyataan",
            created_at=datetime.datetime.now()
        )

        if 'fileKK' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        if 'fileKTP' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        for file in request.files.values():
            content_type = file.filename.split(".")[1]
            filename = f"{str(uuid.uuid4())}.{content_type}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            photo = File(url=filename, letter=new_letter)
            new_letter.files.append(photo)

        db.session.add(new_letter)
        db.session.commit()
        flash('Surat berhasil dikirim', 'success')
        return render_template("pages/letter/surat-pernyataan.html", user=current_user)

    return render_template("pages/letter/surat-pernyataan.html", user=current_user)


@forms.route("/surat-pengantar", methods=["GET", "POST"])
def surat_pengantar():
    if request.method == "POST":
        new_letter = Letter(
            nik=request.form.get('nik'),
            kk=request.form.get('kk'),
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            notes=request.form.get('notes'),
            type="pengantar",
            created_at=datetime.datetime.now()
        )

        if 'fileKK' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        if 'fileKTP' not in request.files.keys():
            flash('Mohon upload foto / scan Kartu Keluarga!', 'error')
            return redirect(request.url)

        for file in request.files.values():
            content_type = file.filename.split(".")[1]
            filename = f"{str(uuid.uuid4())}.{content_type}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            photo = File(url=filename, letter=new_letter)
            new_letter.files.append(photo)

        db.session.add(new_letter)
        db.session.commit()
        flash('Surat berhasil dikirim', 'success')
        return render_template("pages/letter/surat-pengantar.html", user=current_user)

    return render_template("pages/letter/surat-pengantar.html", user=current_user)
