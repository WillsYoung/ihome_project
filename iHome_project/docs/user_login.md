
###  登录接口

####request请求
POST /user/login/
#### params参数：

	mobile str 电话号码/用户名
	possword str 密码

####response响应

####成功响应：
    {'code': OK, 'msg': '请求成功'}

####失败响应1：
    {'code': 900, 'msg': '数据库访问失败'}

####失败响应2：
    {'code': 1005, 'msg': '密码错误'}

####失败响应3：
    {'code': 1001, 'msg': '手机号码错误'}

####失败响应4：
    {'code': 1004, 'msg': '用户不存在'}

