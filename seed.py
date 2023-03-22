"""Seed file for blogly db"""

from models import User, Post, db
from app import app

# Create tables
db.drop_all()
db.create_all()

user1 = User(first_name='Alena', 
             last_name='Vrattos', 
             image_url='https://cdna.artstation.com/p/assets/images/images/034/457/416/small/shin-min-jeong-.jpg?1612345207')
user2 = User(first_name='Min', 
             last_name='DaeHyun', 
             image_url='https://cdnb.artstation.com/p/assets/images/images/034/457/413/small/shin-min-jeong-.jpg?1612345200')

db.session.add(user1)
db.session.add(user2)

db.session.commit()

post1 = Post(title='Welcome', 
             content='Welcome!', 
             user_id=1)
post2 = Post(title='Goodbye', 
             content='Goodbye!', 
             user_id=2)

db.session.add(post1)
db.session.add(post2)

db.session.commit()