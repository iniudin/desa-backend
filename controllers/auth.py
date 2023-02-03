from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Harap periksa detail login Anda dan coba lagi.', "warning")
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        return redirect(url_for('dashboard.statistics'))
    elif request.method == 'GET':
        return render_template('pages/login/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
