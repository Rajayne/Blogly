"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from sqlalchemy import desc
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__,template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.errorhandler(404)
def show_error_page(e):
    return render_template('error.html'), 404

@app.route('/')
def show_home():
    posts = Post.query.order_by(desc('created_at')).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def list_users():
    users = User.query.order_by("first_name").all()
    return render_template('user_list.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('user_form.html')

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
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:id>/edit', methods=['GET'])
def edit_user_form(id):
    user = User.query.get_or_404(id)
    return render_template('user_edit.html', user=user)

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
    tags = Tag.query.order_by('tag_name').all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def new_post_form(id):
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('checks')

    try:
        new_post = Post(title=title, content=content, user_id=id)
        db.session.add(new_post)
        db.session.commit()

        for tag in tags:
            new_posttag = PostTag(post_key=new_post.post_id, tag_key=tag)
            db.session.add(new_posttag)
            db.session.commit()
        return redirect(f'/users/{id}')
    except:
        db.session.rollback()
        return ('Session rolled back on add post, error.')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('post_details.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by('tag_name').all()
    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tags = request.form.getlist('checks')
    new_tags = []

    for tag_name in tags:
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if not tag:
            tag = Tag(tag_name=tag_name)
        new_tags.append(tag)

    post.tags = new_tags
    db.session.commit()
    return redirect(f'/posts/{post_id}')

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
    
@app.route('/tags')
def list_tags():
    tags = Tag.query.order_by('tag_name').all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new', methods=['GET'])
def new_tag_form():
    return render_template('tag_form.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    tag = request.form['tag']

    try:
        new_tag = Tag(tag_name=tag)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(f'/tags')
    except:
        db.session.rollback()
        return (f'Session rolled back on add tag, error. {new_tag}')

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag_edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form['tag']

    try:
        db.session.commit()
        return redirect(f'/tags')
    except:
        db.session.rollback()
        return ('Session rolled back on edit tag, error.')
    
@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    try:
        Tag.get_by_tag_id(tag_id).delete()
        db.session.commit()
        return redirect(f'/tags')
    except:
        db.session.rollback()
        return (f'Session rolled back on delete tag, error.')