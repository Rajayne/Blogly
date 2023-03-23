"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User, Post

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
    users = User.query.order_by("first_name").all()
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
    posts = Post.query.filter_by(user_id=id).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/users/<int:id>/edit', methods=['GET'])
def edit_user_form(id):
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def submit_user_edit(id):
    user = User.query.get_or_404(id)
    previous_image = user.image_url
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or previous_image
    db.session.commit()

    return redirect(f'/users/{id}')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    try:
        User.get_by_id(id).delete()
        db.session.commit()
        return redirect('/users')
    except:
        user = User.query.get_or_404(id)
        db.session.rollback()
        return (f'Session rolled back on delete user, error. {user}, {user.posts}')


@app.route('/users/<int:id>/posts/new', methods=['GET'])
def post_form(id):
    user = User.query.get_or_404(id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def new_post_form(id):
    title = request.form['title']
    content = request.form['content']

    try:
        new_post = Post(title=title, content=content, user_id=id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{id}')
    except:
        db.session.rollback()
        return ('Session rolled back on add post, error.')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    try:
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    except:
        db.session.rollback()
        return ('Session rolled back on edit post, error.')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    user_id = Post.query.get_or_404(post_id).user.id

    try:
        Post.get_by_post_id(post_id).delete()
        db.session.commit()
        return redirect(f'/users/{user_id}')
    except:
        db.session.rollback()
        return (f'Session rolled back on delete post, error.')