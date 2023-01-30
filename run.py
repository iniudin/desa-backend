import os

from flask import Flask
from flask_login import LoginManager

from app import db
from controllers import auth, pages, letter
from models.user import User

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(letter)
app.register_blueprint(pages)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

# with app.app_context():
#     from werkzeug.security import generate_password_hash
#
#     db.create_all()
#     user = User(
#         email='bukor.jaya@gmail.com',
#         password=generate_password_hash('Bukor12!', method='sha256')
#     )
#
#     db.session.add(user)
#     db.session.commit()

if __name__ == '__main__':
    app.run(port=3000)
