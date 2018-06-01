import re

import os
from flask import Blueprint, redirect, render_template, jsonify, session, request

from ihome_utils.setting import UPLOAD_DIR
from ihome_utils.status_code import *

from authentification.models import User, House, Area, Facility, db, HouseImage, Order

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/myhouse/')
def myhouse():
    return render_template('myhouse.html')


@house_blueprint.route('/auth_myhouse/')
def auth_myhouse():
    user = User.query.get(session['user_id'])
    if user.id_card:

        houses = House.query.filter(House.user_id == user.id).order_by(House.id.desc())
        house_list = []
        for house in houses:
            house_list.append(house.to_dict())
        return jsonify(house_list=house_list, code=200)
    else:
        return jsonify(MYHOUSE_USER_IS_NOT_AUTH)


@house_blueprint.route('/newhouse/')
def newhouse():
    return render_template('newhouse.html')


@house_blueprint.route('/newhouse/', methods=['POST'])
def publish_newhouse():

    newhouse = request.form
    title = newhouse.get('title')
    price = newhouse.get('price')
    area_id = newhouse.get('area_id')
    address = newhouse.get('address')
    room_count = newhouse.get('room_count')
    acreage = newhouse.get('acreage')
    unit = newhouse.get('unit')
    capacity = newhouse.get('capacity')
    beds = newhouse.get('beds')
    deposit = newhouse.get('deposit')
    min_days = newhouse.get('min_days')
    max_days = newhouse.get('max_days')

    facility_ids = newhouse.getlist('facility')

    # 将房屋信息填入到数据库的房屋表
    # 找到发布房源的 user
    user = User.query.get(session['user_id'])

    house = House(user.id, area_id, title, price, address, room_count, acreage,
                 unit, capacity, beds, deposit, min_days, max_days)

    if facility_ids:
        facis = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facis

    try:
        house.add_update()
        return jsonify(code=200, house_id=house.id)
    except Exception as e:
        print(e)
        return jsonify(DATABASE_ERROR)

    # 房屋配置信息id 与房屋id 的多对多关系表填写
    # faci_list = []
    # for facility in facilities:
    #     faci = Facility.query.filter(Facility.id == facility).first()
    #     faci.houses.append(house)
    #     faci_list.append(faci)
    # try:
    #     db.session.add_all(faci_list)
    #     db.session.commit()
    #     return jsonify(code=200, house_id=house.id)
    # except Exception as e:
    #     print(e)
    #     return jsonify(DATABASE_ERROR)


@house_blueprint.route('/newhousepicture/', methods=['POST'])
def newhouse_picture():
    picture = request.files

    if 'house_image' in picture:
        picture_path = picture.get('house_image')

        # 判断上传图片类型
        if not re.match(r'^image/.*$', picture_path.mimetype):
            return jsonify(USER_UPLOAD_PICTURE_IS_ERROR)

        # 获得上传图片的url
        url = os.path.join(UPLOAD_DIR, picture_path.filename)
        picture_path.save(url)

        image_url = os.path.join('/static/upload', picture_path.filename)

        house_id = request.form.get('house_id')
        # 根据房屋id，给房屋的index_image_url 字段赋值
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = image_url
            try:
                house.add_update()
            except Exception as e:
                print(e)
                return jsonify(DATABASE_ERROR)

        house_image = HouseImage()
        house_image.house_id = house_id
        house_image.url = image_url

        try:
            house_image.add_update()
            return jsonify(code=OK, url=image_url)
        except Exception as e:
            print(e)
            return jsonify(DATABASE_ERROR)


@house_blueprint.route('/area_facility/')
def area_facility():
    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilities = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilities]

    return jsonify(area_list=area_list, facility_list=facility_list)


@house_blueprint.route('/detail/')
def house_detail_html():

    return render_template('detail.html')


@house_blueprint.route('/detail/<int:id>/')
def house_details_api(id):

    house = House.query.get(id)

    booking = 1
    if house.user_id == session['user_id']:
        booking = 0

    return jsonify(code=200, house=house.to_full_dict(), booking=booking)


@house_blueprint.route('/booking/')
def booking():
    return render_template('booking.html')


@house_blueprint.route('/booking/<int:id>/')
def booking_house(id):
    house = House.query.get(id)
    return jsonify(code=200, house=house.to_dict())


@house_blueprint.route('/index/')
def index():
    return render_template('index.html')


@house_blueprint.route('/hindex/')
def house_index():
    """展示app的首页信息，
    通过异步访问数据库，渲染出首页的房屋图片等信息
    """
    username = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        username = user.name

    houses = House.query.order_by(House.id.desc())[:5]
    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]
    return jsonify(code=200, username=username,
                   hlist=hlist, alist=alist)


@house_blueprint.route('/search/')
def search():
    return render_template('search.html')


@house_blueprint.route('/allsearch/')
def house_search():

    search_dict = request.args

    area_id = search_dict.get('aid')
    start_date = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_key = search_dict.get('sk')

    if not all([area_id, start_date, end_date]):
        return jsonify(PARAMS_ERROR)

    # 先获取所有房屋
    # 对不符合条件的房屋进行处理，先从已有的订单过滤掉一部分房屋
    houses = House.query
    orders = Order.query.filter(start_date < Order.begin_date, end_date > Order.end_date).all()
    orders += Order.query.filter(end_date <= Order.end_date, end_date >= Order.begin_date).all()
    orders += Order.query.filter(start_date >= Order.begin_date, start_date <= Order.end_date).all()

    order_list = [order.house_id for order in orders]
    houses = houses.filter(House.id.notin_(order_list))
    # 排除当前所选时间已经有订单的房屋，剩下的就是可以展示的房屋
    houses = houses.filter(House.area_id == area_id)
    # 然后再从所有可以展示的房屋中找出当前所选择的区域的房屋

    # 将符合条件的房屋按照对应的 url请求排序
    if sort_key:
        if sort_key == 'booking':
            sort_key = House.order_count.desc()
        elif sort_key == 'price-inc':
            sort_key = House.price.asc()
        elif sort_key == 'price-des':
            sort_key = House.price.desc()
    else:
        sort_key = House.id.desc()
    houses = houses.order_by(sort_key)
    # 将符合条件的房屋对象变为json格式序列化的数据
    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=200, alist=alist, hlist=hlist)
