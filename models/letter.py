from datetime import datetime

from app import db


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kk = db.Column(db.String(16), nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(255), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    files = db.relationship('File', backref='letter', lazy=True, cascade="all, delete")


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    letter_id = db.Column(db.Integer, db.ForeignKey('letter.id', ondelete="cascade"), nullable=False)
