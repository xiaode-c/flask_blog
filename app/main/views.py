# coding:utf-8
import datetime
from flask import render_template, url_for, request, flash, redirect
from flask.ext.login import login_required, current_user
from . import main
from .. import login_manager
from ..models import User, Post, Category, Tag

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@main.route("/", methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    title = "Index"
    pagination = Post.query.paginate(page, 10, False)
    posts = pagination.items
    posts.reverse()
    categorys = Category.query.all()
    tags = Tag.query.all()
    return render_template("index.html", title=title, tags=tags, categorys=categorys, posts=posts, pagination=pagination)

@main.route("/detail/<int:id>", methods=['GET', 'POST'])
def detail(id):
    post = Post.query.get_or_404(id)
    return render_template('detail.html', post=post)


@main.route("/categorys/<int:id>")
def categorys(id):
    tags = Tag.query.all()
    categorys = Category.query.all()
    category = Category.query.get(id)
    return render_template('categorys.html', category=category, categorys=categorys, tags=tags)

@main.route("/tags/<tag_name>")
def tags(tag_name):
    tags = Tag.query.all()
    categorys = Category.query.all()
    tag = Tag.query.filter_by(tag_name=tag_name).all()
    tag_posts = []
    for t in tag:
        tag_posts.extend(t.posts)
    tag_posts.reverse()
    return render_template('tags.html', tags=tags, categorys=categorys, tag_posts=tag_posts)

@main.route("/about")
def about():
    categorys = Category.query.all()
    tags = Tag.query.all()
    return render_template('about.html', tags=tags, categorys=categorys)
