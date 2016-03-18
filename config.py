# coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #这里user指mysql用户名,一般是root; password是user的密码;host为主机地址,本地时一般为localhost; db_name为你的数据库名，需要事先建好
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'mysql://user:password@host/dbname'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Hello World"
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
