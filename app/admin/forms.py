# coding:utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, DateTimeField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField(u'用户名:', validators=[Required()])
    password = PasswordField(u'密码:', validators=[Required()])
    remember_me = BooleanField(u'记住')
    submit = SubmitField(u'登录')