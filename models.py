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
                           nullable=False,
                           required=True)
    
    last_name = db.Column(db.String(15),
                          nullable=False,
                          required=True)
    
    image_url = db.Column(db.String(256),
                          nullable=False
                          default='')
    