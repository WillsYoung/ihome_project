###  注册接口

####request请求
POST /user/regist/
#### params参数：

	mobile str 电话号码
	possword str 密码
	possword2 str 密码


####response响应

####成功响应：
    {'code': 200, 'msg': '请求成功'}

####失败响应1：
    {'code': 900, 'msg': '数据库访问失败'}

####失败响应2：
   {'code': 1000, 'msg': '注册信息参数错误'}

####失败响应3：
    {'code': 1001, 'msg': '手机号码错误'}

####失败响应4：
    {'code': 1001, 'msg': '手机号码已注册'}

####失败响应5：
    {'code': 1001, 'msg': '注册密码不一致'}