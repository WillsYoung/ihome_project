###修改用户个人信息接口

###request
PUT /user/profile/
####params 参数：
  form object 表单
  files object 上传文件
 
####成功响应
  {'code': 200, 'msg': '请求成功'}
  
####失败响应 1：
  {'code': 1006, 'msg': '上传图片不符合标准'}
  
####失败响应 2：  
  {'code': 1007, 'msg': '用户名已存在'}

####失败响应 3：
  {'code': 900, 'msg': '数据库访问失败'}
  
####失败响应 4：
  {'code': 901, 'msg': '参数错误'}