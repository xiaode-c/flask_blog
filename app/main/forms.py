# coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, DateTimeField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

# class AddTagForm():
#     tag_name = StringField(u'tagName')
#     submit = SubmitField(u'pub')

# class AddCategoryForm(object):
#     category_name = StringField(u'CategoryName')
#     submit = SubmitField(u'pub')
        
        

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[Required()])
    password = PasswordField(u'密码:', validators=[Required()])
    remember_me = BooleanField(u'记住')
    submit = SubmitField(u'登录')

# class AddPostForm(Form):
#     title = StringField(u"标题", validators=[Required()])
#     body = PageDownField(u"内容", validators=[Required()])
#     pub_date = DateTimeField(u"修改时间")
#     categorys = Select()
#     submit = SubmitField(u"pub")

# class CommentForm(Form):
#     comment_author = StringField(u'作者', validators=[Required()])
#     comment_body = StringField(u'评论内容', validators=[Required()])
#     submit = SubmitField(u'评论')