###ihome首页接口


####request请求(渲染首页)
GET /house/hindex/

####params 参数：  
####    无

####response响应

####成功响应：
  {
   'code': 200,
   'usernmae':'username 用户姓名',
   'hlist': 'hlist 需要渲染房屋信息的序列化数据',
   'alist': 'alist 需要渲染房屋地址的序列化数据'
   }

#### 失败响应：

####request请求：
GET /house/search/?aid=& sd=& ed=&
####params参数：
    aid int 当前所选择区域 id
    sd  datetime 开始时间
    ed  datetime 结束时间
    
####成功响应：

  {
   'code': 200,
   'usernmae':'username 用户姓名',
   'hlist': 'hlist 需要渲染房屋信息的序列化数据',
   'alist': 'alist 需要渲染房屋地址的序列化数据'
   }
    
####失败响应：
    {'code': 901, 'msg': '参数错误'}
    
    
 