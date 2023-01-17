import os
from datetime import timedelta, datetime

import bcrypt
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# SQL CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return f'<User {self.name}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return f'<Letter {self.name}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nik': self.nik,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


with app.app_context():
    db.create_all()


def password_hash(password):
    byte_password = password.encode('utf-8')
    # Generate salt
    salt = bcrypt.gensalt()
    # Hash password
    return bcrypt.hashpw(byte_password, salt)


def password_check(password, hash_password):
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hash_password)


@app.route('/')
def hello_world():
    return render_template("pages/home.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        try:
            user = User.query.filter_by(email=email).first()
            match_password = password_check(password, user.password)
            if user and match_password:
                access_token = create_access_token(identity=email)
                return jsonify(
                    {
                        'status': 'success',
                        'message': 'berhasil melakukan pendaftaran',
                        'data': {
                            'user': user.to_json(),
                            'accessToken': access_token
                        }
                    }
                )
            else:
                return jsonify({
                    'status': 'fail',
                    'message': 'password salah'
                }), 401

        except IntegrityError:
            return jsonify({
                'status': 'fail',
                'message': 'email salah'
            }), 401
    elif request.method == 'GET':
        return render_template('pages/login.html')


@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    name = request.json.get('name', None)
    password = request.json.get('password', None)

    data = User(name=name, email=email, password=password_hash(password))

    try:
        db.session.add(data)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {
                'status': 'fail',
                'message': 'email telah digunakan'
            }
        ), 401

    access_token = create_access_token(identity=email)
    return jsonify(
        {
            'status': 'success',
            'message': 'Berhasil melakukan pendaftaran',
            'data': {
                'user': data.to_json(),
                'accessToken': access_token
            }
        }
    )


@app.route('/letters', methods=['POST'])
def create_letter():
    name = request.json.get('name', None)
    nik = request.json.get('nik', None)
    notes = request.json.get('notes', None)

    data = Letter(name=name, nik=nik, notes=notes)

    try:
        db.session.add(data)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {
                'status': 'fail',
                'message': 'bad requests'
            }
        ), 401

    return jsonify(
        {
            'status': 'success',
            'message': 'berhasil mengirim surat',
            'data': {
                'surat': data.to_json(),
            }
        }
    )


@app.route('/letters', methods=['GET'])
def get_letters():
    letters = [i.to_json() for i in Letter.query.all()]
    return jsonify(
        {
            'status': 'success',
            'message': 'berhasil mengambil surat',
            'data': {
                'surat': letters,
            }
        }
    )


@app.route('/letters/<int:letter_id>', methods=['GET'])
def get_letter_by_id(letter_id):
    letters = Letter.query.filter_by(id=letter_id).first()
    return jsonify(
        {
            'status': 'success',
            'message': 'berhasil mengambil surat',
            'data': {
                'surat': letters.to_json(),
            }
        }
    )


@app.route('/letters/<int:letter_id>', methods=['PUT'])
def update_letter(letter_id):
    letter = Letter.query.filter_by(id=letter_id).first()

    name = request.json.get('name', None)
    nik = request.json.get('nik', None)
    notes = request.json.get('notes', None)
    letter.name = name
    letter.nik = nik
    letter.notes = notes

    try:
        db.session.commit()
        return jsonify(
            {
                'status': 'success',
                'message': 'berhasil menghapus surat'
            }
        ), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {
                'status': 'fail',
                'message': 'id surat tidak ditemukan'
            }
        ), 401


@app.route('/letters/<int:letter_id>', methods=['DELETE'])
def delete_letter(letter_id):
    letter = Letter.query.filter_by(id=letter_id).first()
    try:
        db.session.delete(letter)
        db.session.commit()
        return jsonify(
            {
                'status': 'success',
                'message': 'berhasil menghapus surat'
            }
        ), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {
                'status': 'fail',
                'message': 'id surat tidak ditemukan'
            }
        ), 401


if __name__ == '__main__':
    app.run(debug=True)
