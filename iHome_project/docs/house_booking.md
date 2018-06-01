###房屋预定接口
####reqest请求
POST /order/
####params参数：
    id int 当前预定房间的id
    start_time datetime 当前预定房间的开始时间
    end_time datetime 当前预定房间的结束时间

####response响应：

####成功响应：
  {  
   'code': 200,  
   'order_id': 'id 当前订单的id'  
  }
####失败响应1：
  {  
   'code': 3000,  
   'msg': '创建订单时间有误'  
  }
####失败响应2：
  {  
   'code': 901,  
   'msg': '参数错误'  
  }
    