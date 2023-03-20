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
def show_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('form.html')

# @app.route('/users/new', methods=['POST'])
# def add_new_user():

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
