"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
import urllib.request
from PIL import Image
from models import db, connect_db, User

app = Flask(__name__,template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def show_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    default_url = 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png'
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or default_url

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:id>')
def view_user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)


# @app.route('/users/<int:user_id>/edit', methods=['GET'])
# def edit_user_form():

# @app.route('/users/<int:user_id>/edit', methods=['POST'])
# def submit_user_edit():

# @app.route('/users/<int:user_id>/delete')
# def delete_user():
