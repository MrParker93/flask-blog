import functools
from .models import db, User, Post
from sqlalchemy.exc import IntegrityError
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
                # Adds a new user to the database
                new_user = User(
                    username=username,
                    password=password,
                )

                db.session.add(new_user)
                db.session.commit()
                flash('Successfully created an account', 'success')
                return redirect(url_for('auth.login'))

            except IntegrityError:
                flash('Username already exists. Please use a different one', 'danger')
    
    return render_template('auth/register.html')

# Handles user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username:

            # Query the users table and checks if username exists
            user = User.query.filter_by(username=username).first()

            if user.verify_password(password):
                flash('Successfully logged in.', 'success')
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                flash('Incorrect username or password', 'danger')

        elif not username and password:
            flash('Missing field: Username', 'danger')

        elif username and not password:
            flash('Missing field: Password', 'danger')

        else:
            flash('Missing fields: Username and Password', 'danger')
    
    return render_template('auth/login.html')

# Handles user logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))