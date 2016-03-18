# coding:utf-8
import os
from app import create_app, db
from app.models import User, Post, Tag, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Category=Category)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def initdb():
    db.drop_all()
    db.create_all()

    user = User(name=u"admin",password="123456")
    default = Category(category_name=u"默认")
    db.session.add(user)
    db.session.add(default)
    db.session.commit()

if __name__=="__main__":
    manager.run()
