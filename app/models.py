# coding:utf-8
import datetime
from flask.ext.login import UserMixin
from app import db
#import bleach


post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('posts.id'))
    )

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50))

    def __repr__(self):
        return '<tag: %r>' % self.tag_name

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return '<category name %r>' % self.category_name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modify_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    comment_num = db.Column(db.Integer, default=0)
    view_num = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    categorys = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'), lazy='select')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    tags_name = db.Column(db.Text)


    def __repr__(self):
        return '<post: %r>' % self.title

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    #下面是Flask-Login需要的方法
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #User类中自动添加的id
    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name
# class Comment(db.Model):
#     __tablename__ = 'comment'
#     query_class = CommentQuery
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#     posts = db.relationship(
#         'Post', backref=db.backref('comments', lazy='dynamic'))
#     author_name = db.Column(db.String(50))
#     author_email = db.Column(db.String(100))
#     author_url = db.Column(db.String(1024))
#     author_ip = db.Column(db.String(20))
#     comment_create_time = db.Column(db.DateTime, default=datetime.utcnow)
#     content = db.Column(db.Text)
#     isvisible = db.Column(db.Integer, default=0)

#     def __init__(self, *args, **kwargs):
#         super(Comment, self).__init__(*args, **kwargs)

#     def __repr__(self):
#         return '<comment %r>' % self.content
