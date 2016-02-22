#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 xym
#
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.redis import Redis

from config import config, run_env

db = SQLAlchemy()
csrf = CsrfProtect()
redis = Redis()


def create_app(config_name=None):
    app = Flask(__name__)
    if not config_name:
        config_name = run_env
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    redis.init_app(app)

    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        app.config['LOG_PATH'],
        maxBytes=1024 * 1024,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    from .wechat import wechat as wechat_blueprint
    app.register_blueprint(wechat_blueprint)
    from .flow import flow as flow_blueprint
    app.register_blueprint(flow_blueprint)

    return app
