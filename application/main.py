from .auth import login_required
from .models import db, User, Post
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from flask import Blueprint, flash, redirect, render_template, request,\
            url_for, make_response, g

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    print(f'posts: {posts}')
    print(f'id: {current_user.id}')
    return render_template('main/profile.html', username=current_user.username, posts=posts)
