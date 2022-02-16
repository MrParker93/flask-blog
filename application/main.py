from .auth import login_required
from .models import db, Post
from sqlalchemy.exc import OperationalError, IntegrityError
from flask_login import login_required, current_user
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort
)

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def index():
    search_query = request.args.get('query')
    if search_query:
        posts = Post.search_posts(search_query).all()        
    else:
        posts = Post.query.all()
    return render_template('main/index.html', post=posts)


@bp.route('/profile/id/<int:user_id>/', methods=['GET'])
@login_required
def profile(user_id):
    search_query = request.args.get('query')
    if search_query:
        posts = Post.search_posts(search_query).all()        
    else:
        posts = Post.query.filter(user_id == current_user.id).all()
    return render_template(
        'main/profile.html', username=current_user.username, post=posts,
        id=current_user.id
    )


def create_or_edit_post(template, post):
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.published = True if request.form.get('publish') else False
        post.slug = post.title

        if not (post.title and post.content):
            flash('A title and content are required', 'danger')
        else:
            try:
                db.session.add(post)
                db.session.commit()

            except (IntegrityError, OperationalError):
                flash('An error occured, please try again', 'danger')
                db.session.rollback()
                raise
            else:
                if post.published:
                    flash('Successfully created a post!', 'success')
                    return redirect(url_for('main.post', slug=post.slug))
                else:
                    flash('Successfully created a post!', 'success')
                    return redirect(url_for('main.edit_post', slug=post.slug))
                        
    return render_template(template, post=post)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    return create_or_edit_post(
        'main/create.html', Post(title='', content='', user_id=current_user.id)
    )


@bp.route('/drafts', methods=['GET'])
@login_required
def drafts():
    posts = Post.drafted_posts().order_by(Post.created.desc()).all()
    return render_template('main/drafts.html', post=posts)


@bp.route('/<slug>/', methods=['GET'])
@login_required
def post(slug):
    post = (
        Post.published_posts().filter(Post.slug == slug, Post.user_id == current_user.id).one_or_none()
    )
    if post is None:
        error = 'Post does not exist.'
        return redirect(url_for('main.error', error=error))
    return render_template('main/post.html', post=post)


@bp.route('/edit/<slug>', methods=['GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug, Post.user_id == current_user.id).first()
    return create_or_edit_post('main/edit.html', post)

@bp.route('/delete/<slug>', methods=['GET', 'DELETE'])
@login_required
def delete_post(slug):
    deleted_post = Post.delete_post(slug)
    print(f'deleted:{deleted_post}')
    try:
        db.session.delete(deleted_post)
        db.session.commit()
    except (IntegrityError, OperationalError):
        flash('An error occured, please try again', 'danger')
        db.session.rollback()
        raise
    flash('Post successfully deleted!', 'success')
    return redirect(url_for('main.index'))
    
    
@bp.route('/<error>/error', methods=['GET'])
def error(error):
    return render_template('main/error.html', error=error)