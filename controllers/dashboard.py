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
    keterangan_letter_count = Letter.query.filter(Letter.type == "keterangan").count()
    keterangan_letter_done_count = Letter.query.filter(Letter.is_done.is_(True), Letter.type == "keterangan").count()
    keterangan_letter_not_done_count = Letter.query.filter(Letter.is_done.is_(False),
                                                           Letter.type == "keterangan").count()

    pernyataan_letter_count = Letter.query.filter(Letter.type == "pernyataan").count()
    pernyataan_letter_done_count = Letter.query.filter(Letter.is_done.is_(True), Letter.type == "pernyataan").count()
    pernyataan_letter_not_done_count = Letter.query.filter(Letter.is_done.is_(False),
                                                           Letter.type == "pernyataan").count()

    pengantar_letter_count = Letter.query.filter(Letter.type == "pengantar").count()
    pengantar_letter_done_count = Letter.query.filter(Letter.is_done.is_(True), Letter.type == "pengantar").count()
    pengantar_letter_not_done_count = Letter.query.filter(Letter.is_done.is_(False), Letter.type == "pengantar").count()

    letter_count = Letter.query.count()
    letter_done_count = Letter.query.filter(Letter.is_done.is_(True), ).count()
    letter_not_done_count = Letter.query.filter(Letter.is_done.is_(False)).count()

    return render_template("pages/dashboard/statistics.html", user=current_user, stats={
        'letter_count': letter_count,
        'letter_done': letter_done_count,
        'letter_not_done': letter_not_done_count,
        'keterangan_letter_count': keterangan_letter_count,
        'keterangan_letter_done': keterangan_letter_done_count,
        'keterangan_letter_not_done': keterangan_letter_not_done_count,
        'pernyataan_letter_count': pernyataan_letter_count,
        'pernyataan_letter_done': pernyataan_letter_done_count,
        'pernyataan_letter_not_done': pernyataan_letter_not_done_count,
        'pengantar_letter_count': pengantar_letter_count,
        'pengantar_letter_done': pengantar_letter_done_count,
        'pengantar_letter_not_done': pengantar_letter_not_done_count
    })


@dashboard.route("/surat/keterangan")
@login_required
def surat_keterangan():
    data = Letter.query.filter(Letter.type == 'keterangan').order_by(Letter.created_at.desc()).all()
    return render_template("pages/letter/list.html", datas=data)


@dashboard.route("/surat/pernyataan")
@login_required
def surat_pernyataan():
    data = Letter.query.filter(Letter.type == 'pernyataan').order_by(Letter.created_at.desc()).all()
    return render_template("pages/letter/list.html", datas=data)


@dashboard.route("/surat/pegantar")
@login_required
def surat_pengantar():
    data = Letter.query.filter(Letter.type == 'pengantar').order_by(Letter.created_at.desc()).all()
    return render_template("pages/letter/list.html", datas=data)
