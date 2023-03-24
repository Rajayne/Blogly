"""Seed file for blogly db"""

from models import User, Post, Tag, PostTag, db
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

post1 = Post(title='Irasshaimase', 
             content='Welcome!', 
             user_id=1)
post2 = Post(title='Ohayogozaimas', 
             content='Good Morning!', 
             user_id=1)
post3 = Post(title='Arigatogozaimasu', 
             content='Thank you!', 
             user_id=1)
post4 = Post(title='Joh-eun achim-ieyo', 
             content='Good Night!', 
             user_id=2)
post5 = Post(title='Annyeonghi gaseyo', 
             content='Goodbye!',
             user_id=2)
post6 = Post(title='Cheonman-eyo', 
             content="You're welcome!",
             user_id=2)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)
db.session.commit()

tag1 = Tag(tag_name='yolo')
db.session.add(tag1)
db.session.commit()

posttag1 = PostTag(tag_key=1, post_key=1)
db.session.add(posttag1)
db.session.commit()