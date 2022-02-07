from application import db
from datetime import datetime
from application import _bcrypt as bc
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

# post_comments = Table('comments', db.metadata,
#                 db.Column('user_id',
#                           db.Integer,
#                           db.ForeignKey('users.id',
#                                         ondelete='CASCADE',
#                                         onupdate='CASCADE'),
#                           primary_key=True
#                     ),
#                 db.Column('post_id',
#                           db.Integer,
#                           db.ForeignKey('posts.id',
#                                         ondelete='CASCADE',
#                                         onupdate='CASCADE'),
#                           primary_key=True
#                     ))


# Create database tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(30), unique=True, nullable=False)
    _password = db.Column('password', db.Text, nullable=False)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', back_populates='user',
                cascade='all, delete, delete-orphan')

    @hybrid_property
    def password(self):
        """
        Property of the User class used to define different
        functions called from the same interface.
        """
        return self._password

    @password.setter
    def password(self, password) -> None:
        """
        Receives the password entered by the user as a string and
        converts it to bytes before passing it through the hash function.
        Stores the hashed password.
        """
        self._password = bc.generate_password_hash(password, rounds=12)

    def __repr__(self):
        return '<User(id="%d", username="%s", password="%s", posts="%s")>' %\
                 (self.id, self.username, self.password, self.posts)

    def verify_password(self, password) -> bool:
        """
        Checks the validity of the users password against the
        current password hash and verifies they are identical.
        :param password: str
        :return: bool
        """
        return bc.check_password_hash(self._password, password)

    def change_username(self, username, new_username, password) -> str:
        """
        Verifies the users login details and changes the current username,
        to the new username if available.
        :param username: str
        :param new_username: str
        :param password: str
        :return: str
        """
        pass

    def delete_account(self, username, password) -> None:
        """
        Verifies the users login details and deletes the current
        account from the database.
        :param username: str
        :param password: str
        :return: None"""
        pass


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(80), nullable=False)
    slug = db.Column('slug', db.String(80), unique=True)
    content = db.Column('content', db.Text, nullable=False)
    published = db.Column('published', db.Boolean, index=True)
    created = db.Column('created', db.DateTime, nullable=False,
                    default=datetime.utcnow, index=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return '<Post(id="%d", title="%s", slug="%s", content="%s", user_id="%d")>' \
            % (self.id, self.title, self.slug, self.content, self.user_id)

    def publish(self, *args, **kwargs):
        """
        Checks the `post.published` flag is `True` and publishes
        the post else, save it as a draft to be published.
        """
        pass

    @classmethod
    def published_posts(cls):
        """
        Searches through all posts of current user and displays all
        published posts."""
        pass

    @classmethod
    def drafted_posts(cls):
        """
        Searches through all posts of current user and displays all
        drafted posts."""
        pass

    @classmethod
    def search_posts(cls, query):
        """
        Query the post table for all posts matching the requested search
        query then display all posts in the search result"""
        pass


# class Comment(db.Model):
#     __tablename__ = 'comments'
#     user_id = db.Column(db.Integer, 
#                         db.ForeignKey('users.id',
#                                        ondelete='CASCADE',
#                                        onupdate='CASCADE'),
#                         primary_key=True)
#     post_id = db.Column(db.Integer,
#                         db.ForeignKey('posts.id',
#                                        ondelete='CASCADE',
#                                        onupdate='CASCADE'),
#                         primary_key=True)
#     created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
#                         index=True)
#     content = db.Column(db.Text, nullable=False)

#     def __init__(self, content=None, **kwargs):
#         super(Comment, self).__init__(**kwargs)
#         self.content = content

#     def __repr__(self):
#         return '<Comment(content="%s", user_id="%d", post_id="%d")>'\
#             % (self.content, self.user_id, self.post_id)

#     def comment(self):
#         """
#         Posts a comment under a blog post.
#         """
#         pass

#     @classmethod
#     def edit_comment(self):
#         """
#         Edit the current selected comment.
#         """
#         pass

#     @classmethod
#     def delete_comment(self):
#         """
#         Delete the current selected comment.
#         """
#         pass