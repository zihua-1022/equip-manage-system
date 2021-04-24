import datetime
import threading
from common.exts import db
from common.searchData import CJsonEncoder, cursor, database, r, srch_hash_data
from flask import (Blueprint, flash, json, jsonify, redirect, render_template,
                   request, session, url_for)
from model.models import equipment, information, wx_user
from controller.user import getOpenid

# 实例化一个蓝图
equipapp=Blueprint('equipeapp',__name__,template_folder="../templates",static_folder="../static")
SEPARATOR="<SEPARATOR>"#分隔符

@equipapp.route('/equip_list/<infor_id>')
def equip_list(infor_id):
    return render_template('equip_info.html')

@equipapp.route('/unread_data/<equip_id>')
def unread_data(equip_id):
    return render_template('unread_data.html')

@equipapp.route('/equip_ment/')
def equip_ment():
    return render_template('equipment.html')


#微信小程序删除未读消息（需增加）
@equipapp.route('/wx_del_unreaddata/',methods=["GET","POST"],strict_slashes=False)
def wx_del_unreaddata():
    openid = request.values.get('openid')
    wxuser=wx_user.query.filter(wx_user.wx_id==openid).first()
    wxuser_id=wxuser.id
    id=request.values.get('id')
    sql='delete from information where image_id=%s and user_id=%s' %(id,wxuser_id)
    try:
        cursor.execute(sql)
    except:
        database.ping(reconnect=True)
        cursor.execute(sql)
    
    database.commit()
    return ''

#微信小程序获取设备数据
@equipapp.route('/get_deserve/',methods=['GET','POST'])
def get_deserve():
    exist = r.exists('eq_data')
    if exist==0:
        sql = 'select *from equipment'
        cursor.execute(sql)
        
        user_data = cursor.fetchall()
        json_data = json.dumps(user_data, cls=CJsonEncoder)
        r.set('eq_data',json_data)
    else:
        json_data=r.get('eq_data')
    return json_data

# 微信获取所有设备的未读信息数量()
@equipapp.route('/wx_get_equip_data/',methods=["GET","POST"],strict_slashes=False)
def wx_get_equip_data():
    openid = request.values.get('openid')
    wu = wx_user.query.filter(wx_user.wx_id == openid).first()  #获取用户名
    wxuser_id = wu.id  #获取用户ID
    equip_unread = []
    database.ping(reconnect=True)
    counter_lock2 = threading.Lock()
    counter_lock2.acquire()
    sql = 'select id from equipment'
    cursor.execute(sql)
    # try:
    #     cursor.execute(sql)
    # except:
    #     database.ping(reconnect=True)
    #     cursor.execute(sql)
    data=cursor.fetchall()
    for (i,) in data:
        sql='select count(*) from information where user_id=%s and equip_id=%s'%(wxuser_id,i)
        cursor.execute(sql)
        one=cursor.fetchall()
        for (i,) in one:
            equip_unread.append(i)
    counter_lock2.release()
    equip_unread_data=json.dumps(equip_unread)
    return equip_unread_data

#微信小程序获取已读未读信息的信息id
@equipapp.route('/wx_get_data/',methods=['GET','POST'])
def wx_get_data():
    openid = request.values.get('openid')
    eqid=request.values.get('eqid')
    page = int(request.values.get('page'))
    
    showList = int(request.values.get('showList'))
    page_x = (page - 1) * showList
    page_y=page*showList
    wxuser=wx_user.query.filter(wx_user.wx_id==openid).first()
    wxuser_id = wxuser.id
    
    #获取未读信息数量
    sql = 'select  count(*) from information where user_id=%s and equip_id=%s' % (wxuser_id, eqid)
    cursor.execute(sql)
    unread_num = cursor.fetchall()
    #去除tuple数组的括号，例：将(1,)变成1
    for (i,) in unread_num:
        unread_num=i
    #获取未读信息id
    sql='select image_id from information where user_id=%s and equip_id=%s' %(wxuser_id,eqid)
    try:
        cursor.execute(sql)
    except:
        database.ping(reconnect=True)
        cursor.execute(sql)
    image_id = cursor.fetchall()
    unreadId=''
    if image_id==():
        return ''
    else:
        for (i,) in image_id:
            unreadId += '%s,' % i
        unreadId = unreadId[0:-1]
        #联合查询，先查询未读信息再查询已读信息，分别加上不同的字段区分已读未读
        sql='(select *,false as state, \'red\' as color from upload_img where id in (%s) ORDER BY date desc LIMIT %s)\
        UNION ALL\
        (select *,true,\'green\' from upload_img where not id in (%s) ORDER BY date desc LIMIT 100) limit %s,%s;'%(unreadId,unread_num,unreadId,page_x,page_y)
        
        cursor.execute(sql)
        unread_data = cursor.fetchall()
  
        json_data=json.dumps(unread_data,cls=CJsonEncoder)
        return json_data
        


#微信小程序删除未读消息（需增加）
@equipapp.route('/del_unreaddata/',methods=["GET","POST"],strict_slashes=False)
def del_unreaddata():
    openid = request.values.get('openid')
    wxuser=wx_user.query.filter(wx_user.wx_id==openid).first()
    wxuser_id=wxuser.id
    id=request.values.get('id')
    sql='delete from information where image_id=%s and user_id=%s' %(id,wxuser_id)
    try:
        cursor.execute(sql)
    except:
        database.ping(reconnect=True)
        cursor.execute(sql)
    
    database.commit()
    return ''
# 获取设备名称和设备码
@equipapp.route('/wx_getEqm/',methods=['GET','POST'])
def wx_getEqm():
    sql = 'select equip_name,equip_code from equipment'
    cursor.execute(sql)
    data = cursor.fetchall()
    json_data=json.dumps(data,cls=CJsonEncoder)
    return json_data


# 小程序获取设备相关信息
@equipapp.route('/getImformation/',methods=['GET','POST'])
def getimformation():
    Eqid = request.values.get('eqid')
    Unread = request.values.get('unread_id')
    database.ping(reconnect=True)
    counter_lock2 = threading.Lock()
    counter_lock2.acquire()
    if Unread == '[]':
        sql = 'select * from upload_img where equip_id=%s order by date desc' % Eqid
        cursor.execute(sql)
        data = cursor.fetchall()
        json_data=json.dumps(data,cls=CJsonEncoder)
        return json_data
    else:
        Unread=Unread[1:-1]
        
        sql = 'select *from upload_img where not id in (%s) ORDER BY date desc;' % Unread
        cursor.execute(sql)
        data=cursor.fetchall()
        json_data=json.dumps(data,cls=CJsonEncoder)
        return json_data
    # if exist==0:
    #     sql='select * from upload_img where equip_id=%s order by date desc' %Eqid
    #     try:
    #         cursor.execute(sql)
    #     except:
    #         database.ping(reconnect=True)
    #         cursor.execute(sql)
    #     data=cursor.fetchall()
        
    #     message=[]
    #     y=[]
    #     for i in data:    
    #         wxuser=wx_user.query.filter(wx_user.id==i[1]).first()
    #         name=wxuser.name 
    #         y.append(i[0])
    #         y.append(name)
    #         y.append(i[2])
    #         y.append(i[3]) 
    #         y.append(i[5]) 
    #         y.append(i[6])  
    #         message.append(y)
    #         y=[]
    #     json_data=json.dumps(message,cls=CJsonEncoder)
    #     counter_lock2.release()
    #     r.set("eqimfo"+Eqid,json_data)  
    #     return json_data       
    # else:
    #     return r.get("eqimfo"+Eqid)
        
    # eqinf=information.query.filter(information.equip_id==Eqid).all()




# 获取所有设备的未读信息数量（缓存，修改过）
@equipapp.route('/get_equip_data/',methods=["GET","POST"],strict_slashes=False)
def get_equip_data():
    userid = request.args.get('userID')
    user_name = r.get(userid)
    wu = wx_user.query.filter(wx_user.name == user_name).first()  #获取用户名
    wxuser_id = wu.id  #获取用户ID
    equip_unread=[]
    data = r.sort('equip:id',by='equipment:*->id', get=['equipment:*->id'])
    for equip_id in data:           
        sql='select count(*) from information where user_id=%s and equip_id=%s'%(wxuser_id,equip_id)
        cursor.execute(sql)
        one=cursor.fetchall()
        for (i,) in one:
            equip_unread.append(i)
    equip_unread_data=json.dumps(equip_unread)
    return equip_unread_data

# 获取所有设备的具体信息(缓存，修改过)
@equipapp.route('/get_equip_detail_data/',methods=["GET","POST"],strict_slashes=False)
def get_equip_detail_data():
    equip_unread_data = srch_hash_data('equipment','init','None')
    return equip_unread_data


# 获取用户点击设备对应的未读信息
@equipapp.route('/get_unread_data/',methods=['GET','POST'])
def get_unread_data():
    userid = request.args.get('userID')
    eq_id = request.args.get('equipID')
    user_name = r.get(userid)
    wu = wx_user.query.filter(wx_user.name == user_name).first()  #获取用户名
    wxuser_id = wu.id  #获取用户ID
    sql='select image_id from information where user_id=%s and equip_id=%s' %(wxuser_id,eq_id)
    cursor.execute(sql)
    image_id=cursor.fetchall()
    unread_arr=[]
    for (i,) in image_id:
        unread_data = srch_hash_data('upload_img','id',str(i))
        unread_arr.append(unread_data[0][0])
        unread_arr.append(unread_data[0][1])  
        unread_arr.append(unread_data[0][2])      
    json_data=json.dumps(unread_arr,cls=CJsonEncoder)
    return json_data

# 获取用户点击设备对应的已读信息
@equipapp.route('/get_is_data/',methods=['GET','POST'])
def get_is_data():
    userid = request.args.get('userID')
    eq_id = request.args.get('equipID')
    user_name = r.get(userid)
    wu = wx_user.query.filter(wx_user.name == user_name).first()  #获取用户名
    wxuser_id = wu.id  #获取用户ID
    sql='select image_id from information where user_id=%s and equip_id=%s' %(wxuser_id,eq_id)
    cursor.execute(sql)
    image_id=cursor.fetchall()
    all_id=[]
    unread_id=[]
    for (i,) in image_id:
        unread_id.append(i)
    imgs_id = srch_hash_data('upload_img','equip_id',eq_id)
  
    for i in imgs_id:
        all_id.append(i)
    # 将所有的图片id减去未读图片的id获得已读图片的ID
    is_id=set(all_id)-set(unread_id)
    read_arr=[]
    for i in is_id:
        read_data = srch_hash_data('upload_img','id',str(i))
        read_arr.append(read_data[0][0])
        read_arr.append(read_data[0][1])  
        read_arr.append(read_data[0][2])       
    json_data=json.dumps(read_arr,cls=CJsonEncoder)
    return json_data

# 查看用户选中的该条未读信息的具体信息(缓存，修改过)
@equipapp.route('/del_unread_data/')
def del_unread_data():
    userid = request.args.get('userID')
    infor_id = request.args.get('inforID')
    read_flag = request.args.get('read_flag')
    if read_flag == 'unread_id':
        user_name = r.get(userid)
        wu = wx_user.query.filter(wx_user.name == user_name).first()  #获取用户名
        wxuser_id = wu.id  #获取用户ID
        sql='delete from information where image_id=%s and user_id=%s' %(infor_id,wxuser_id)
        cursor.execute(sql)
        database.commit()
    data = srch_hash_data('imgs','id',infor_id)
    return data
 


##############以下为客户端发送显微镜当前的工作状态代码###############
# C#客户端开机上传设备信息/设备关机判断工作状态(有问题？)
@equipapp.route('/cs_equipment/', methods=['GET', 'POST'],strict_slashes=False)
def equip_infor():
    received=request.get_data()
    equipInfor=received.decode(encoding="utf8",errors='ignore')
    print(equipInfor)
    equip_name,equip_disc,if_work,equip_adr,equip_ip,equip_posi,equip_code = equipInfor.split("，")
  
    equip = equipment.query.filter(equipment.equip_code == equip_code).first()   
    if not equip:
        equip_data = equipment(equip_name=equip_name,equip_disc=equip_disc,if_work=if_work,
            equip_adr=equip_adr,equip_ip=equip_ip,equip_posi=equip_posi,equip_image=0,equip_code=equip_code)
        db.session.add(equip_data)
        db.session.commit()
    else:
        # if_work = '\'%s\'' % if_work
        # # equip_name = '\'%s\'' % equip_name
        # sql='update equipment set if_work=%s where equip_code=%s' %(if_work,equip_name)
        equ_update = equipment.query.filter(equipment.equip_code == equip_code).update({'if_work': if_work})
        db.session.commit()
    return 'success'
