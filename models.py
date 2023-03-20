from flask_sqlalchemy import SQLAlchemy

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
    
    title = db.Column(db.String(15),
                      nullable=False)
    
    content = db.Column(db.String(15),
                        nullable=False)

    created_at = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'))
    
    @classmethod
    def get_by_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id)