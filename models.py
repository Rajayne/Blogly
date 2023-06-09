from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(15),
                           nullable=False)
    
    last_name = db.Column(db.String(15),
                          nullable=False)
    
    image_url = db.Column(db.String(256),
                          nullable=True)
    
    posts = db.relationship('Post', cascade='all, delete', backref='user')

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id)

    def __repr__(self):
        u = self
        return f'{u.first_name} {u.last_name}'
    
class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(60),
                      nullable=False)
    
    content = db.Column(db.String(256),
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           server_default=func.now())
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE'),
                                      nullable=False)

    tag = db.relationship('Tag', 
                           secondary='post_tags',
                           backref='posts')
    
    @classmethod
    def get_by_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id)
    
    @classmethod
    def get_datetime(cls, post_id):
        post = cls.query.get(post_id)
        datetime = post.created_at.strftime(f'%a %b %d %Y, %I:%M %p')
        return datetime
    
    def __repr__(self):
        p = self
        return f'Title: {p.title}, Content: {p.content}, Created {p.created_at} by {p.user}'
    
class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    
    tag_name = db.Column(db.String(60),
                         nullable=False,
                         unique=True)
    
    post = db.relationship('Post', 
                           secondary='post_tags',
                           backref='tags')

    @classmethod
    def get_by_tag_id(cls, tag_id):
        return cls.query.filter_by(tag_id=tag_id)

    def __repr__(self):
        t = self
        return f'{t.tag_name} {t.post}'    
    
class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_key = db.Column(db.Integer,
                         db.ForeignKey('posts.post_id',
                                       ondelete='CASCADE'),
                                       primary_key=True)
    tag_key = db.Column(db.Integer,
                        db.ForeignKey('tags.tag_id',
                                       ondelete='CASCADE'),
                                       primary_key=True)
    
    @classmethod
    def get_tag_from_key(cls, tag_key):
        return cls.query.filter_by(tag_key=tag_key)
    
    @classmethod
    def get_post_from_key(cls, post_key):
        return cls.query.filter_by(post_key=post_key)

    def __repr__(self):
        x = self
        post = Post.query.get_or_404(x.post_key)
        tag = Tag.query.get_or_404(x.tag_key)
        return (f'Post: {post.title}, Tag: {tag.tag_name}')