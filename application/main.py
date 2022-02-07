from .auth import login_required
from .models import db, User, Post
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from flask import Blueprint, flash, redirect, render_template, request,\
            url_for, make_response, g

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('main/index.html', posts=posts)

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.id).limit(3).all()
    return render_template('main/profile.html', username=current_user.username, posts=posts)

def create_or_edit_post(template, post):
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.published = True if request.form.get('publish') else False

        if not (post.title and post.content):
            flash('A title and content are required', 'danger')
        else:
            try:
                db.session.add(post)
                db.session.commit()
                flash('Successfully created a post!', 'success')

            except IntegrityError:
                flash('An error occured, please try again', 'danger')
            else:
                if post.published:
                    return redirect(url_for('main.post', slug=post.slug))
                else:
                    return redirect(url_for('main.edit_post', slug=post.slug))

    return render_template(template, post=post)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    return create_or_edit_post('main/create.html', Post(title='', content=''))

@bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return create_or_edit_post('main/edit.html', post)
