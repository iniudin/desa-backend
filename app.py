import os
from datetime import timedelta, datetime

import bcrypt
from flask import Flask, request, jsonify
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
            'password': self.password.decode('utf-8'),
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
    return jsonify(code=200, message='Server running'), 200


@app.route('/login', methods=['POST'])
def login():
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
                    'message': 'Berhasil melakukan pendaftaran',
                    'data': {
                        'user': user.to_json(),
                        'accessToken': access_token
                    }
                }
            )
        else:
            return jsonify({'msg': 'password salah'}), 401

    except AttributeError:
        return jsonify({'msg': 'email salah'}), 401


@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    name = request.json.get('name', None)
    password = request.json.get('password', None)

    try:
        data = User(name=name, email=email, password=password_hash(password))
        db.session.add(data)
        db.session.commit()
    except IntegrityError:
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


@app.route('/dashboard')
def dashboard():
    return jsonify(code=200, message='Dashboard'), 200


@app.route('/letter')
def letter():
    return jsonify(code=200, message='Surat'), 200


if __name__ == '__main__':
    app.run(debug=True)
