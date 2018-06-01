
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask import session, redirect

db = SQLAlchemy()
se = Session()


def init_ext(app):

    db.init_app(app)
    se.init_app(app)


def get_database_uri(DATABASE):
    """
    将数据库的URI拼接起来
    :param DATABASE:
    :return: 连接数据库的uri
    """
    host = DATABASE.get('host')
    db = DATABASE.get('db')
    driver = DATABASE.get('driver')
    port = DATABASE.get('port')
    user = DATABASE.get('user')
    password = DATABASE.get('password')
    name = DATABASE.get('name')

    return '{}+{}://{}:{}@{}:{}/{}'.format(
        db, driver, user, password, host, port, name)


import functools


def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            # 验证用户是否登录
            # if 'user_id' in session:
            if session['user_id']:
                return view_fun()
            else:
                return redirect('/user/login/')

        except Exception as e:
            print(e)
            return redirect('/user/login/')

    return decorator