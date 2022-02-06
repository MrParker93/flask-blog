from application import db
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy


# Create database tables
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_comments = db.relationship('Comment', cascade='all, delete-orphan',
                                backref='user')

    comments = association_proxy('user_comments', 'user')

    # def __init__(self, username, password, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     self.username = username
    #     self.password = password

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
        pass

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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), unique=True)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, index=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    comments_on_post = db.relationship('Comment', cascade='all, delete-orphan',
                                       backref='post')
                            
    comments = association_proxy('comments_on_post', 'post')

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


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id',
                                       ondelete='CASCADE',
                                       onupdate='CASCADE'),
                        primary_key=True)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id',
                                       ondelete='CASCADE',
                                       onupdate='CASCADE'),
                        primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                        index=True)
    content = db.Column(db.Text)

    def __init__(self, user, post, content=None, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.user_id = user.id
        self.post_id = post.id
        self.content = content

    def __repr__(self):
        return '<Comment(id="%d", content="%s", user_id="%d", post_id="%d")>'\
            % (self.id, self.content, self.user_id, self.post_id)

    def comment(self):
        """
        Posts a comment under a blog post.
        """
        pass

    @classmethod
    def edit_comment(self):
        """
        Edit the current selected comment.
        """
        pass

    @classmethod
    def delete_comment(self):
        """
        Delete the current selected comment.
        """
        pass