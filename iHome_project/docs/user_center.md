###用户个人中心接口

####个人中心接口
####request请求
PUT POST /user/profile

####    params参数：
        request.form object 表单
        retquest.files object 上传文件对象

####成功响应：
    {'code': 200, 'msg': '请求成功'}

####失败响应1：
    {'code': 900, 'msg': '数据库访问失败'}
####失败响应2：
    {'code': 1006, 'msg': '上传图片不符合标准'}
####失败响应3：
    {'code': 1007, 'msg': '用户名已存在'}
####失败响应4：
    {'code': 901, 'msg': '参数错误'}


###修改个人信息接口
###request请求
PUT /user/


####上传request请求
GET /user/auths
无参数
####成功响应：
    return jsonify(code=200, id_card=user.id_card, id_name=user.id_name)

####失败响应：
    {'code': 901, 'msg': '参数错误'}

