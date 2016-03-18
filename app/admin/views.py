# coding:utf-8

from . import admin
from flask import render_template, url_for, request, flash, redirect
from .. import db, login_manager
from ..models import User, Post, Category, Tag
from flask.ext.login import login_required, login_user, logout_user, current_user
from .forms import LoginForm
import mistune


def add_article(title, content, body, author_id, tags, category_id, tags_name):
    """
    This is a method for add post
    """
    post = Post(title=title, content=content, body=body, author_id=author_id, category_id=category_id, tags=tags, tags_name=tags_name)
    db.session.add(post)
    db.session.commit()
    print "添加文章完成"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@admin.route("/")
@login_required
def index():
    return render_template("admin/index.html")

@admin.route("/posts")
@login_required
def posts():
    posts = Post.query.all()
    return render_template("admin/posts.html", posts=posts)

@admin.route('/comments')
@login_required
def comments():
    return render_template("admin/comments.html")

@admin.route("/categorys")
@login_required
def categorys():
    categorys = Category.query.all()
    return render_template("admin/categorys.html", categorys=categorys)

@admin.route("/tags")
@login_required
def tags():
    tags = Tag.query.all()
    return render_template("admin/tags.html", tags=tags)

@admin.route("/users")
def users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)

@admin.route("/add-post", methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["body"]
        markdown = mistune.Markdown()
        body = markdown(content)
        author_id = current_user.id
        category_id = request.form['category']
        tag_string = request.form['tags']
        tag_list = request.form['tags'].split(',')
        tags = []
        for tag in tag_list:
            tags.append(Tag(tag_name=tag))

        add_article(title=title, content=content, body=body, author_id=author_id, tags=tags, category_id=category_id, tags_name=tag_string)
    categories = Category.query.all()
    return render_template("admin/add-post.html", categories=categories)

@admin.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("admin/edit-post.html", post=post)
    else:
        post.title = request.form["title"]
        content = request.form["body"]
        post.content = content
        markdown = mistune.Markdown()
        post.body=markdown(content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("admin.posts"))




@admin.route('/posts/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.id==post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("admin.posts"))

@admin.route("/add-tag", methods=['GET', 'POST'])
@login_required
def add_tag():
    if request.method == 'GET':
        return render_template(url_for("admin.tags"))
    else:
        tag_name = request.form["tag_name"]
        tag = Tag(tag_name=tag_name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('admin.tags'))

@admin.route('/tags/<int:tag_id>/delete', methods=['GET'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.filter(Tag.id==tag_id).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return redirect(url_for("admin.tags"))

@admin.route("/add-category", methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'GET':
        return render_template(url_for("admin.categorys"))
    else:
        category_name = request.form["category_name"]
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin.categorys"))

@admin.route('/categorys/<int:category_id>/delete', methods=['GET'])
@login_required
def delete_category(category_id):
    category = Category.query.filter(Category.id==category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for("admin.categorys"))

@admin.route("/add-user", methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'GET':
        return render_template(url_for("admin.users"))
    else:
        user_name = request.form["user_name"]
        password = request.form["password"]
        email = request.form["email"]
        user = User(name=user_name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.users"))

@admin.route('/users/<int:user_id>/delete', methods=['GET'])
@login_required
def delete_user(user_id):
    user = User.query.filter(User.id==user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin.users"))


@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(name=username).first()
        if user is not None:
            login_user(user, remember_me)
            return redirect(request.args.get('next') or url_for("admin.index"))
        flash('Invalid username or password')
    return render_template("login.html", form=form)

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

    return "logout"
