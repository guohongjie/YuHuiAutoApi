#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config.config import config
from flask_redis import FlaskRedis
from flask_login import LoginManager
from celery import Celery
bootstrap = Bootstrap()
db = SQLAlchemy()
redis = FlaskRedis()
login_manager = LoginManager()
login_manager.login_view = "user.userLogin"

def make_celery(app):
    celery = Celery(app.import_name,broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
    celery.Task = ContextTask
    return celery
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.update(CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='redis://localhost:6379/2')
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)
    from app.main import report,test,views,mock,user,flow
    app.register_blueprint(report, url__prefix='/report')
    app.register_blueprint(test)
    app.register_blueprint(views)
    app.register_blueprint(mock)
    app.register_blueprint(user)
    app.register_blueprint(flow)
    return app
