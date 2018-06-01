
from flask import Blueprint, request, render_template, session, jsonify
from datetime import datetime

from authentification.models import Order, House, User
from ihome_utils.status_code import *

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/', methods=['POST'])
def order_apif():
    """提交订单
    """

    order_dict = request.form
    house_id = order_dict.get('house_id')
    start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
    end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')

    if not all([house_id, start_time, end_time]):
        return jsonify(PARAMS_ERROR)

    if start_time > end_time:
        return jsonify(ORDER_START_TIME_GT_END_TIME)

    house = House.query.get(house_id)
    # 这里选择房间后需要判断，房屋时间是否正确
    for order in house.orders:
        if (order.end_date >= end_time and order.begin_date <= end_time) or \
                (order.end_date >= start_time and order.begin_date <= start_time) or \
                (order.begin_date > start_time and order.end_date < end_time):
            return jsonify(PARAMS_ERROR)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days + 1
    order.amount = order.days * order.house_price

    order.add_update()

    return jsonify(code=200, order_id=order.id)


@order_blueprint.route('/order/')
def orders_html():
    return render_template('orders.html')


@order_blueprint.route('/order/<int:id>/')
def orders_apif(id):
    """获取订单的信息
    """
    # 找到下单的用户
    if id == 0:
        user = User.query.get(session['user_id'])
        orders = user.orders
        orders_api = []
        for order in orders:
            order_api = order.to_dict()
            house = House.query.get(order.house_id).to_dict()
            orders_api.append({'order': order_api, 'house': house})
    else:
        order = Order.query.get(id)
        house = House.query.get(order.house_id)
        orders_api = [{'order': order.to_dict(), 'house': house.to_dict()}]
        id = house.id
    return jsonify(code=200, orders=orders_api, id=id)


@order_blueprint.route('/lorders/')
def lorders_html():
    """
    跳转到客户的订单页面
    :return:
    """
    return render_template('lorders.html')


@order_blueprint.route('/fd/')
def lorder_fd():
    # 第一种方式
    # 通过当前登录用户发布的所有房屋查询id
    houses = House.query.filter(House.user_id == session['user_id'])
    houses_ids = [house.id for house in houses]
    # 通过房屋 id查找所有的订单
    orders = Order.query.filter(Order.house_id.in_(houses_ids)).order_by(Order.id.desc())
    olist = [order.to_dict() for order in orders]

    # 第二种方式，利用多对多的关系房屋与订单
    # houses = House.query.filter(House.user_id == session['user_id'])
    # order_list = []
    # for house in houses:
    #     orders = house.orders
    #     order_list.append(orders)

    return jsonify(olist=olist, code=200)


@order_blueprint.route('/order/<int:id>/', methods=['PATCH'])
def order_status(id):
    """房东对客户订单信息进行修改，是/否接单
    id 表示正在处理的订单的 id
    """
    status = request.form.get('status')
    order = Order.query.get(id)
    order.status = status

    if status == 'REJECTED':
        comment = request.form.get('comment')
        order.comment = comment

    try:
        order.add_update()
        return jsonify(code=200)
    except:
        return jsonify(DATABASE_ERROR)


