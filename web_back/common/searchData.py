import datetime
import json
import redis
import pymysql


# 创建数据库连接,password='root'
database = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='root',
                           db='wechat_demo',
                           charset='utf8',
                           autocommit=True)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = database.cursor()

r=redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)



# 创建一个视图
v_sql = 'create or replace view v_userImgs as select wx_user.name,upload_img.*,imgs.data_path \
    from upload_img left join wx_user on wx_user.id=upload_img.user_id left join imgs on upload_img.id=imgs.upload_id'
cursor.execute(v_sql)

v_sql = 'create or replace view v_upImgs as select imgs.id,imgs.upload_id,upload_img.image_desc,\
    upload_img.image_title,imgs.file_path,imgs.data_path from imgs left join upload_img on upload_img.id=imgs.upload_id'
cursor.execute(v_sql)





# # 按时间查找数据
# def search_time(time, types):
#     if types == 'wx_user':
#         userData=[]
#         for k in r.scan_iter('wx_user*'):
#             r_date = r.hget(k,'date')
#             if time == r_date[0:10]:
#                 data = r.hmget(k,'id','name','phone','email','password','wx_id')
#                 userData.append(data)
#         userData = tuple(userData)
#         json_data = json.dumps(userData,cls=CJsonEncoder)
#     elif types == 'upload_img':
#         imgsData=[]
#         for k in r.scan_iter('upload_img*'):
#             r_date = r.hget(k,'date')
#             if time == r_date[0:10]:
#                 data = r.hmget(k,'name','id','user_id','number','equip_id','image_desc','image_title','date')
#                 imgsData.append(data)
#         imgsData = tuple(imgsData)
#         json_data = json.dumps(imgsData,cls=CJsonEncoder)
#     else:
#         logsData=[]
#         for k in r.scan_iter('logs*'):
#             r_date = r.hget(k,'date')
#             if time == r_date[0:10]:
#                 data = r.hmget(k,'id','name','number','date')
#                 logsData.append(data)
#         logsData = tuple(logsData)
#         json_data = json.dumps(logsData,cls=CJsonEncoder)
#     return json_data

# # 按名字查找数据
# def search_name(name, types):
#     if types == 'wx_user':
#         userData=[]
#         for k in r.scan_iter('wx_user*'):
#             r_username = r.hget(k,'name')
#             if name == r_username:
#                 data = r.hmget(k,'id','name','phone','email','password','wx_id')
#                 userData.append(data)
#         userData = tuple(userData)
#         json_data = json.dumps(userData,cls=CJsonEncoder)
#     elif types == 'upload_img':
#         imgsData=[]
#         for k in r.scan_iter('upload_img*'):
#             r_username = r.hget(k,'name')
#             if name == r_username:
#                 data = r.hmget(k,'name','id','user_id','number','equip_id','image_desc','image_title','date')
#                 imgsData.append(data)
#         imgsData = tuple(imgsData)
#         json_data = json.dumps(imgsData,cls=CJsonEncoder)
#     else:
#         logsData=[]
#         for k in r.scan_iter('logs*'):
#             r_username = r.hget(k,'name')
#             if name == r_username:
#                 data = r.hmget(k,'id','name','number','date')
#                 logsData.append(data)
#         logsData = tuple(logsData)
#         json_data = json.dumps(logsData,cls=CJsonEncoder)
#     return json_data


# 时间类型数据转json格式所用的类方法
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
      
#根据什么获取相应的数据
def srch_hash_data(key_name,types,flag):

    if types is 'id':
        if key_name == 'imgs':
            imgsData = []
            if len(r.keys('imgs*')) == 0:
                sql = 'select * from v_upImgs'
                cursor.execute(sql)
                print("初始化id")
                data=cursor.fetchall()
                for i in range(len(data)):
                    imgs_infor = {'id':data[i][0],'upload_id':data[i][1],'image_desc':data[i][2],'image_title':data[i][3],'file_path':data[i][4]}
                    r.hmset('imgs:%d'%(data[i][0]),imgs_infor)
                    r.expire('imgs:%d'%(data[i][0]),432000)
            print("查询缓存id")
            for k in r.scan_iter('imgs*'):
                r_imgsid = r.hget(k,'upload_id')
                if flag == r_imgsid:
                    data = r.hmget(k,'image_desc','image_title','file_path')
                    imgsData.append(data)
            imgsData = tuple(imgsData)
            imgsData = json.dumps(imgsData,cls=CJsonEncoder)
            return imgsData
        else:
            if len(r.keys('upload_img*')) == 0:
                sql='select distinct * from v_userImgs'
                cursor.execute(sql)
                print("初始化id")
                imgsData=cursor.fetchall()
                for i in range(len(imgsData)):
                    imgs_infor = {'name':imgsData[i][0],'id':imgsData[i][1],'user_id':imgsData[i][2],'number':imgsData[i][3],
                        'date':imgsData[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':imgsData[i][5],'image_desc':imgsData[i][7],'image_title':imgsData[i][6],'data_path':imgsData[i][8]}
                    r.lpush('upimgs:id',imgsData[i][1])
                    r.expire('upimgs:id',432000)
                    r.hmset('upload_img:%d'%(imgsData[i][1]),imgs_infor)
                    r.expire('upload_img:%d'%(imgsData[i][1]),432000)          
            jsonData=[]
            print("查询缓存id")
            for k in r.scan_iter('upload_img*'):
                r_id = r.hget(k,'id')
                if flag == r_id:
                    data = r.hmget(k,'id','number','date')
                    jsonData.append(data)
            jsonData = tuple(jsonData)
            return jsonData

    elif types is 'equip_id':
        if key_name == 'upload_img':
            if len(r.keys('upload_img*')) == 0:
                sql='select distinct * from v_userImgs'
                cursor.execute(sql)
                print("初始化")
                imgsData=cursor.fetchall()
                for i in range(len(imgsData)):
                    imgs_infor = {'name':imgsData[i][0],'id':imgsData[i][1],'user_id':imgsData[i][2],'number':imgsData[i][3],
                        'date':imgsData[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':imgsData[i][5],'image_desc':imgsData[i][7],'image_title':imgsData[i][6],'data_path':imgsData[i][8]}
                    r.lpush('upimgs:id',imgsData[i][1])
                    r.expire('upimgs:id',432000)
                    r.hmset('upload_img:%d'%(imgsData[i][1]),imgs_infor)
                    r.expire('upload_img:%d'%(imgsData[i][1]),432000)
            print("查询缓存")
            jsonData = []
            for k in r.scan_iter('upload_img*'):
                r_equipid = r.hget(k,'equip_id')
                if flag == r_equipid:
                    data = r.hget(k,'id')
                    jsonData.append(int(data))
            jsonData = tuple(jsonData)
            return jsonData

    elif types is 'name':
        if key_name == 'wx_user':
           
            if len(r.keys('wx_user*')) == 0:
                sql='select * from wx_user'
                cursor.execute(sql)
                print("初始化")
                userData=cursor.fetchall()
                for i in range(len(userData)):
                    user_infor = {'id':userData[i][0],'name':userData[i][1],'phone':userData[i][2],'email':userData[i][3],
                        'password':userData[i][4],'wx_id':userData[i][5]}
                    r.hmset('wx_user:%d'%(userData[i][0]),user_infor)
                    r.expire('wx_user:%d'%(userData[i][0]),432000)
            userData=[]
            for k in r.scan_iter('wx_user*'):
                r_username = r.hget(k,'name')
                if flag == r_username:
                    data = r.hmget(k,'id','name','phone','email','password','wx_id')
                    userData.append(data)
            userData = tuple(userData)
            json_data = json.dumps(userData,cls=CJsonEncoder)
        elif key_name == 'upload_img':
            
            if len(r.keys('upload_img*')) == 0:
                sql='select distinct * from v_userImgs'
                cursor.execute(sql)
                print("初始化")
                imgsData=cursor.fetchall()
                for i in range(len(imgsData)):
                    imgs_infor = {'name':imgsData[i][0],'id':imgsData[i][1],'user_id':imgsData[i][2],'number':imgsData[i][3],
                        'date':imgsData[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':imgsData[i][5],'image_desc':imgsData[i][7],'image_title':imgsData[i][6],'data_path':imgsData[i][8]}
                    r.hmset('upload_img:%d'%(imgsData[i][1]),imgs_infor)
                    r.expire('upload_img:%d'%(imgsData[i][1]),432000)
            imgsData=[]
            for k in r.scan_iter('upload_img*'):
                r_username = r.hget(k,'name')
                if flag == r_username:
                    data = r.hmget(k,'name','id','user_id','number','date','equip_id','image_desc','image_title','data_path')
                    imgsData.append(data)
            imgsData = tuple(imgsData)
            json_data = json.dumps(imgsData,cls=CJsonEncoder)
        else:
            logsData=[]
            for k in r.scan_iter('logs*'):
                r_username = r.hget(k,'name')
                if flag == r_username:
                    data = r.hmget(k,'id','name','number','date')
                    logsData.append(data)
            logsData = tuple(logsData)
            json_data = json.dumps(logsData,cls=CJsonEncoder)
        return json_data

    elif types is 'date':   
        jsonData=[]
        if key_name == 'wx_user':
            # userData=[]
            if len(r.keys('wx_user*')) == 0:
                sql='select * from wx_user'
                cursor.execute(sql)
                print("初始化")
                userData=cursor.fetchall()
                for i in range(len(userData)):
                    user_infor = {'id':userData[i][0],'name':userData[i][1],'phone':userData[i][2],'email':userData[i][3],
                        'password':userData[i][4],'wx_id':userData[i][5]}
                    r.hmset('wx_user:%d'%(userData[i][0]),user_infor)
                    r.expire('wx_user%d:'%(userData[i][0]),432000)

            for k in r.scan_iter('wx_user*'):
                r_date = r.hget(k,'date')
                if flag == r_date[0:10]:
                    data = r.hmget(k,'id','name','phone','email','password','wx_id')
                    jsonData.append(data)
            jsonData = tuple(jsonData)
            # json_data = json.dumps(jsonData,cls=CJsonEncoder)
        elif key_name == 'upload_img':
            # imgsData=[]
            if len(r.keys('upload_img*')) == 0:
                sql='select distinct * from v_userImgs'
                cursor.execute(sql)
                print("初始化")
                imgsData=cursor.fetchall()
                for i in range(len(imgsData)):
                    imgs_infor = {'name':imgsData[i][0],'id':imgsData[i][1],'user_id':imgsData[i][2],'number':imgsData[i][3],
                        'date':imgsData[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':imgsData[i][5],'image_desc':imgsData[i][7],'image_title':imgsData[i][6],'data_path':imgsData[i][8]}
                    r.hmset('upload_img:%d'%(imgsData[i][1]),imgs_infor)
                    r.expire('upload_img:%d'%(imgsData[i][1]),432000)

            for k in r.scan_iter('upload_img*'):
                r_date = r.hget(k,'date')
                if flag == r_date[0:10]:
                    data = r.hmget(k,'name','id','user_id','number','date','equip_id','image_desc','image_title','data_path')
                    jsonData.append(data)
            jsonData = tuple(jsonData)
            # json_data = json.dumps(jsonData,cls=CJsonEncoder)
        else:
            # logsData=[]
            for k in r.scan_iter('logs*'):
                r_date = r.hget(k,'date')
                if flag == r_date[0:10]:
                    data = r.hmget(k,'id','name','number','date')
                    jsonData.append(data)
            jsonData = tuple(jsonData)
        json_data = json.dumps(jsonData,cls=CJsonEncoder)
        return json_data
    
    elif types is 'init':
        if key_name == 'wx_user':
            if len(r.keys('wx_user*')) == 0:
                sql='select * from wx_user'
                cursor.execute(sql)
                print("初始化用户")
                userData=cursor.fetchall()
                for i in range(len(userData)):
                    user_infor = {'id':userData[i][0],'name':userData[i][1],'phone':userData[i][2],'email':userData[i][3],
                        'password':userData[i][4],'wx_id':userData[i][5]}
                    r.hmset('wx_user:%d'%(userData[i][0]),user_infor)
                    r.expire('wx_user:%d'%(userData[i][0]),432000)
            else:
                print("查询缓存")
                userData = []
                for k in r.scan_iter('wx_user*'):
                    data = r.hmget(k,'id','name','phone','email','password','wx_id')
                    userData.append(data)
                userData = tuple(userData)
            userData = json.dumps(userData,cls=CJsonEncoder)
            return userData
        elif key_name == 'upload_img':
            if len(r.keys('upload_img*')) == 0:
                sql='select distinct * from v_userImgs'
                cursor.execute(sql)
                print("初始化图片")
                imgsData=cursor.fetchall()
                for i in range(len(imgsData)):
                    imgs_infor = {'name':imgsData[i][0],'id':imgsData[i][1],'user_id':imgsData[i][2],'number':imgsData[i][3],
                        'date':imgsData[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':imgsData[i][5],'image_desc':imgsData[i][7],'image_title':imgsData[i][6],'data_path':imgsData[i][8]}
                    r.hmset('upload_img:%d'%(imgsData[i][1]),imgs_infor)
                    r.expire('upload_img:%d'%(imgsData[i][1]),432000)
            else:
                print("查询缓存")
                imgsData = []
                for k in r.scan_iter('upload_img*'):
                    data = r.hmget(k,'name','id','user_id','number','date','equip_id','image_desc','image_title','data_path')
                    imgsData.append(data)
                imgsData = tuple(imgsData)
            imgsData = json.dumps(imgsData,cls=CJsonEncoder)
            return imgsData
        else:
            if len(r.keys('equipment*')) == 0:
                print("初始化设备")
                sql='select * from equipment'
                cursor.execute(sql)
                equipData=cursor.fetchall()
                # equip_unread_data=json.dumps(equipData)
                for i in range(len(equipData)):
                    equip_infor = {'id':equipData[i][0],'equip_name':equipData[i][1],'equip_disc':equipData[i][2],'if_work':equipData[i][3],
                        'equip_adr':equipData[i][4],'equip_ip':equipData[i][5],'equip_posi':equipData[i][6],'equip_img':equipData[i][7],'equip_code':equipData[i][8]}
                    r.lpush('equip:id',equipData[i][0])
                    r.expire('equipment',2592000)
                    r.hmset('equipment:%d'%(equipData[i][0]),equip_infor)
                    r.expire('equipment:%d'%(equipData[i][0]),2592000)
            else:
                print("查询缓存")
                data = r.sort('equip:id',by='equipment:*->id', get=['equipment:*->id',
                    'equipment:*->equip_name','equipment:*->equip_disc','equipment:*->if_work',
                    'equipment:*->equip_adr','equipment:*->equip_ip','equipment:*->equip_posi','equipment:*->equip_img','equipment:*->equip_code'],groups=True)
                equipData = tuple(data)
            equip_unread_data = json.dumps(equipData)
            return equip_unread_data

    else:
        if key_name == 'wx_user':
            pass
        else:
            for i in flag:
                for k in r.scan_iter('imgs*'):
                    r_imgsid = r.hget(k,'id')
                    if i == r_imgsid:
                        print("删除缓存")
                        r.delete(k)
                sql = 'delete from imgs where upload_id=%s;' % i
                cursor.execute(sql)
                database.commit()
        for i in flag:
            for k in r.scan_iter(''+key_name+'*'):
                r_userid = r.hget(k,'id')
                if i == r_userid:
                    print("删除缓存")
                    r.delete(k)
            sql = 'delete from ' + key_name + ' where id=%s;' % i
            cursor.execute(sql)
            database.commit()

        json_data = []
        for k in r.scan_iter(''+key_name+'*'):
            if key_name == 'wx_user':
                data = r.hmget(k,'id','name','phone','email','password','wx_id')
            else:
                data = r.hmget(k,'name','id','user_id','number','equip_id','image_desc','image_title','date')
            json_data.append(data)
        json_data = tuple(json_data)
        json_data = json.dumps(json_data,cls=CJsonEncoder)
        return json_data
        




    