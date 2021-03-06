from .models import db, User
from sqlalchemy.exc import IntegrityError

from flask_login import login_user, logout_user, login_required
from flask import Blueprint, flash, redirect, render_template, request,\
             url_for

bp = Blueprint('auth', __name__, url_prefix='/auth')

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

            except IntegrityError:
                flash('Username already exists. Please use a different one', 'danger')
            else:
                return redirect(url_for('auth.login'))

    
    return render_template('auth/register.html')

# Handles user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_session = True if request.form.get('remember') else False

        if username and password:

            # Query the users table and checks if username exists
            user = User.query.filter_by(username=username).first()

            if user is None:
                flash('Incorrect username or password', 'danger')
            elif user.verify_password(password):
                flash('Successfully logged in.', 'success')
                login_user(user, remember=remember_session)
                return redirect(url_for('main.profile'))

        elif not username and password:
            flash('Missing field: Username', 'danger')

        elif username and not password:
            flash('Missing field: Password', 'danger')

        else:
            flash('Missing fields: Username and Password', 'danger')
    
    return render_template('auth/login.html')

# Handles user logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

