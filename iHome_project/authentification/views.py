
import re

import os
from flask import Blueprint, render_template, request, jsonify, session, redirect

from authentification.models import db, User
from ihome_utils.setting import UPLOAD_DIR
from ihome_utils.status_code import *
from ihome_utils.functions import is_login

user = Blueprint('user', __name__)


@user.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':

        return render_template('register.html')

    if request.method == 'POST':

        regist_dict = request.form

        mobile = regist_dict.get('mobile')
        password = regist_dict.get('password')
        password2 = regist_dict.get('password2')

        # 验证所有信息是否提交
        if not all([mobile, password, password2]):
            return jsonify(USER_REGISTER_PARAMS_ERROR)

        # 验证手机号码是否正确
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(USER_REGISTER_MOBILE_ERROR)

        # 验证手机号是否已经存在
        if User.query.filter(User.phone == mobile).count():
            return jsonify(USER_REGISTER_MOBILE_IS_EXIST)

        # 验证两次密码是否一致
        if password != password2:
            return jsonify(USER_REGISTER_PASSWORD_ERROR)

        user = User()
        user.phone = mobile
        user.name = mobile
        user.password = password

        try:
            user.add_update()
            return jsonify(SUCCESS)
        except Exception as e:
            print(e)
            return jsonify(DATABASE_ERROR)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':
        user_dict = request.form

        mobile = user_dict.get('mobile')
        password = user_dict.get('password')

        # 判断是否所有信息都有输入
        if not all([mobile, password]):
            return jsonify(PARAMS_ERROR)

        # 判断电话号码是否正确
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(USER_REGISTER_MOBILE_ERROR)

        # 判断用户名是否存在以及密码是否正确
        user = User.query.filter(User.phone == mobile).first()
        if user:
            if user.check_pwd(password):
                session['user_id'] = user.id
                return jsonify(SUCCESS)
            else:
                return jsonify(USER_LOGIN_PASSWORD_IS_ERROR)
        else:
            return jsonify(USER_IS_NOT_EXIST)


@user.route('/my/', methods=['get'])
@is_login
def my_center():
    """个人中心
    """
    if request.method == 'GET':
        return render_template('my.html')


@user.route('/getuser/', methods=['get'])
@is_login
def get_user():

    if request.method == 'GET':
        id = session['user_id']
        user = User.query.filter(User.id == id).first()

        return jsonify(code=200, user=user.to_basic_dict())


@user.route('/profile/')
@is_login
def profile():

    return render_template('profile.html')


@user.route('/profile/', methods=['PUT'])
@is_login
def user_profile():
    user_dict = request.form
    file_dict = request.files
    if 'avatar' in file_dict:
        f1 = file_dict['avatar']

        # 判断上传图片类型
        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(USER_UPLOAD_PICTURE_IS_ERROR)

        # url 是图片保存在本地的绝对路径
        url = os.path.join(UPLOAD_DIR, f1.filename)
        f1.save(url)

        user = User.query.filter(User.id == session['user_id']).first()
        image_url = os.path.join('/static/upload', f1.filename)
        user.avatar = image_url

        try:
            user.add_update()
            return jsonify(code=OK, url=image_url)
        except Exception as e:
            print(e)
            return jsonify(DATABASE_ERROR)
    elif 'name' in user_dict:
        name = user_dict.get('name')

        if User.query.filter(User.name == name ).count():
            return jsonify(USER_UPDATE_USERNAME_IS_EXIST)

        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(SUCCESS)
        except Exception as e:
            print(e)
            return jsonify(DATABASE_ERROR)
    else:
        return jsonify(PARAMS_ERROR)


@user.route('/getavatar/')
@is_login
def get_avatar():

    user = User.query.filter(User.id == session['user_id']).first()
    return jsonify(url=user.avatar, code=200)


@user.route('/auths/')
@is_login
def auths():
    user = User.query.get(session['user_id'])
    try:
        if user.id_card:
            return jsonify(code=200, id_card=user.id_card, id_name=user.id_name)
    except Exception as e:
        print(e)
        return jsonify(PARAMS_ERROR)


@user.route('/auth/', methods=['PUT', 'POST', 'GET'])
@is_login
def authentication():
    """进行身份实名认证
    """
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')

        if not all([id_name, id_card]):
            return jsonify(PARAMS_ERROR)

        # 验证身份证号码
        if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
            return jsonify(USER_AUTH_IDCARD_IS_ERROR)

        try:
            user = User.query.filter(User.id == session['user_id']).first()
            user.id_name = id_name
            user.id_card = id_card
            user.add_update()
            return jsonify(SUCCESS)
        except Exception as e:
            print(e)
            return jsonify(DATABASE_ERROR)


@user.route('/logout/')
@is_login
def user_logout():
    session.clear()

    return render_template('login.html')


@user.route('/createdb/')
def create_db():
    db.create_all()

    return '创建表格成功'