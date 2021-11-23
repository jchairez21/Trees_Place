from flask import render_template, redirect, session, request, flash
from trees_app import app
from trees_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# THE ABOVE LINE NEEDS CURRENT PROJECT ADJUSTMENTS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    user_id = User.save(data)

    session['logged_user'] = user_id
    # He created a SESSION with a KEY ['logged_user'] SET it EQUALS to LOGGED IN USERS = user_id
    return redirect('/dashboard')


@app.route('/user/login', methods=['POST'])
def login_user():
    data = {
        "email": request.form['email']
    }

    retrieved_user = User.get_email(data)

    if not retrieved_user:
        flash("Invalid email/password", "login_error")
        return redirect('/')

    if not bcrypt.check_password_hash(retrieved_user.password, request.form['password']):
        flash("Invalid email/password", "login_error")
        return redirect('/')

    session['logged_user'] = retrieved_user.id

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
