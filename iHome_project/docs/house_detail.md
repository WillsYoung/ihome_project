### 房屋信息详情接口

#### request请求
GET /house/deatil/&lt;int:id>/
####params参数：
    id int 当前选择房间的id
    
####成功响应：
  {  
   'code': 200,  
   'house': 'house.to_full_dict() 房屋信息的josn数据',  
   'booking': 'booking 标志当前登录是不是发布房间的用户'  
  }
####失败响应：
  无