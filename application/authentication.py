import bcrypt
import functools
from .models import db, User, Post
from sqlite3 import IntegrityError
from datetime import datetime as dt
from flask import current_app as app
from flask import Blueprint, flash, redirect, render_template, request,\
            session, url_for, make_response, g

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Ensures current user's data is loaded before each request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(
            User.id == user_id).first()

# Decorator to check login authentication
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(*args, **kwargs)
    return wrapped_view

# Handles user registration
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        # Ensures username and password fields are not empty
        if not username:
            error = 'Username is required.'
            flash(error, 'danger')

        elif not password:
            error = 'Password is required'
            flash(error, 'danger')
        
        if error is None:
            try:
                # Convert str to bytes to enable password hash
                password = bytes(password, 'UTF-8')
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))

                # Adds a new user to the database
                new_user = User(
                    username=username,
                    password=hashed_password,
                )

                db.session.add(new_user)
                db.session.commit()
                flash('Successfully created an account', 'success')
                return redirect(url_for('auth.login'))

            except IntegrityError:
                flash('Username already taken. Please use a different one', 'danger')
    
    return render_template('auth/register.html')

# Handles user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            hashed_password = bcrypt.hashpw(
                bytes(password, 'UTF-8'), bcrypt.gensalt(12))

            # Query the users table and checks if username exists
            current_user = User.query.filter(
                (User.username == username) & (User.password == bcrypt.checkpw(password, hashed_password))
            ).first()
            
            if current_user:
                flash('Successfully logged in.', 'success')
                session.clear()
                session['user_id'] = current_user.scalar().id
                return redirect(url_for('index'))
            else:
                flash('Incorrect username or password', 'danger')

        elif not username and password:
            flash('Missing field: Username')

        elif username and not password:
            flash('Missing field: Password')

        else:
            flash('Missing fields: Username and Password')
    
    return render_template('auth/login.html')

# Handles user logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))