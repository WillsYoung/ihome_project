###发布新房源接口

####新房源信息接口
####request请求
POST /house/newhouse/

#### params参数：
    form object 表单
    
    
#### response响应

####成功响应：
    {
        'code': 200,
        'house_id': 'house.id 当前发布房屋的id'
    }

####失败响应：
    {
    'code': 900, 
    'msg': '数据库访问失败'
    }

####新房源图片接口  
####request请求
POST /house/newhousepicture/
####paramas参数
    form object 表单
    
####成功响应
    {
        'code': 200,
        'url': 'image_url 图片的路径'
    }
####失败响应 1：
    {'code': 900, 'msg': '数据库访问失败'}
####失败响应 2：
    {'code': 1006, 'msg': '上传图片不符合标准'}
####失败响应 3：
    