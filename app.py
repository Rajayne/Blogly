"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User

app = Flask(__name__,template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)