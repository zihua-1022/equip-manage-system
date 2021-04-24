from flask import Blueprint,request,render_template,url_for,session,json,flash,redirect,jsonify,abort
from common.myForms import LoginForm
from common.exts import db
from model.models import wx_user,webuser
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from flask_mail import Message
from threading import Thread
from flask_login import current_user,login_user
import random
import datetime
import os
import threading
import string
import requests




# 实例化一个蓝图
userapp=Blueprint('userapp',__name__,template_folder="../templates",static_folder="../static")


@userapp.route('/admin_manage/')
def admin_manage():
    return render_template('admin_base.html')

# 用户管理
@userapp.route('/user_manage/')
def user_manage():
    return render_template('usermanage.html')

@userapp.route('/admin_register/user/<arg>', methods=['GET', 'POST'])
def user_register(arg):
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return ''

@userapp.route('/admin_login/<arg>', methods=['GET', 'POST'])
def userlogin(arg):
    if request.method == 'GET':
        if(arg=='admin'):
            return render_template('login.html')
        else:
            return render_template('userVerify.html')
    else:
        return ''


@userapp.route('/userloss/', methods=['GET', 'POST'])
def userloss():
    if request.method == 'GET':
        return render_template('userloss.html')
    else:
        return ''

@userapp.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    else:
        return ''

@userapp.route('/change_email/', methods=['GET', 'POST'])
def change_email():
    if request.method == 'GET':
        return render_template('change_email.html')
    else:
        return ''

@userapp.route('/change_phone/', methods=['GET', 'POST'])
def change_phone():
    if request.method == 'GET':
        return render_template('change_phone.html')
    else:
        return ''

@userapp.route('/personal_cental/', methods=['GET', 'POST'])
def personal_cental():
    if request.method == 'GET':
        return render_template('personal_cental.html')
    else:
        return ''

@userapp.route('/login_index/', methods=['GET', 'POST'])
def login_index():
    if request.method == 'GET':
        return render_template('login_index.html')
    else:
        return ''

@userapp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return ''

# 获取用户数据
@userapp.route('/getuserdata/', methods=['GET', 'POST'])
def getuserdata():
    json_data = srch_hash_data('wx_user','init','None')
    return json_data


# 修改用户数据
@userapp.route('/change_userdata/', methods=['GET', 'POST'])
def changedata():
    userid = request.args.get('id')
    name = request.args.get('name')
    phone = request.args.get('phone')
    email = request.args.get('email')
    u_name = '\'%s\'' % name
    u_phone = '\'%s\'' % phone
    u_mail = '\'%s\'' % email
    if len(r.keys('wx_user*')) != 0:
        for k in r.scan_iter('wx_user*'):
            r_userid = r.hget(k,'id')
            if userid == r_userid:
                print("更新缓存")
                user_infor = {'name':name,'phone':phone,'email':email}
                r.hmset(k,user_infor)
    sql = 'update wx_user set name=%s,phone=%s,email=%s where id=%s' % (u_name, u_phone, u_mail, userid)
    cursor.execute(sql)
    database.commit()
    json_data = srch_hash_data('wx_user','init','None')
    return json_data

def getOpenid():
    return openid

#获取openid(新)
@userapp.route('/loGin/', methods = ['POST','GET'])
def loGin():
    data = json.loads(request.get_data().decode('utf-8')) #将前端Json数据转为字典
    isuser=None
    appID = 'wxe379510271c2fe10' #开发者关于微信小程序的appID
    appSecret = 'c793f56eb3ec5e9baede6580a0c7dcfa' #开发者关于微信小程序的appSecret
    code = data['code'] #前端POST过来的微信临时登录凭证code
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    response_data = requests.get(wx_login_api, params=req_params) #向API发起GET请求
    data = response_data.json()
    # global openid
    openid = data['openid'] #得到用户关于当前小程序的OpenID
    session_key = data['session_key'] #得到用户关于当前小程序的会话密钥session_key
    id=wx_user.query.filter(wx_user.wx_id==openid).first() 
    openidExist= wx_user.query.filter_by(wx_id=openid).first()
    if openidExist:
        isuser=True
    else :
        isuser=False
    return jsonify({'status':'success',
        'session_key':session_key,
        'openid':openid,
        'isuser':isuser
        }) 
   

# 小程序用户注册
@userapp.route('/register/', methods=['POST'])
def register():
    openid=request.values.get('openid')
    username=request.values.get('name')  
    
    id=wx_user.query.filter(wx_user.wx_id==openid).first()
    if id:
        return '该用户已注册'
    else:
        for k in r.scan_iter('wx_user*'):
            r.delete(k)
        user = wx_user(name=username,wx_id=openid,phone='无',email='无',password='123456',info_number=0,control_power=0)
        db.session.add(user)
        db.session.commit()

        for k in r.scan_iter('wx_user*'):
            r.delete(k)
        wxuser=wx_user.query.filter(wx_user.wx_id==openid).first()
        id=wxuser.id
        sql='select * from upload_img' 
        cursor.execute(sql)
        image_id=cursor.fetchall()
        for i in image_id:
            unread="insert into information(user_id,image_id,equip_id) VALUE (%s,%s,%s)" %(id,i[0],i[4])
            # unread = information(user_id=id,image_id=i[0],equip_id=i[4])
            cursor.execute(unread)
        database.commit()
        return ''

#小程序获取个人信息
@userapp.route('/get_personal/',methods=['GET','POST'])
def get_personal():
    openid=request.values.get('openid')
    database.ping(reconnect=True)
    counter_lock2 = threading.Lock()
    counter_lock2.acquire()
    sql="select * from wx_user where wx_id = '" + openid + "'"
    cursor.execute(sql)
    data=cursor.fetchall()
    counter_lock2.release()
    json_data = json.dumps(data, cls=CJsonEncoder)
    return json_data



#验证网页用户帐号密码（缓存，修改过）
#先查询redis是否存在此用户，然后查询mysql数据库有没，如果有（登录成功）把登录的用户名做主健存到redis，密码做值。以后登录就直接查redis
@userapp.route('/check_user/', methods=['POST', 'GET'], strict_slashes=False)
def check_user():
    userphone = request.form.get('userphone')
    pwd = request.form.get('password')
    code = request.form.get('code')
    remem_me = request.form.get('remember_me')
    phone_mail = '\'%s\'' % userphone
    password = '\'%s\'' % pwd
    ran_char = ''.join(random.sample(string.ascii_letters + string.digits, 6))#新增加的
    # if len(r.keys('wx_user*')) == 0:
    sql = 'select name from wx_user where phone=%s and password=%s or email=%s and password=%s' %(phone_mail,password,phone_mail,password)
    cursor.execute(sql)
    userdata = cursor.fetchall()
    # userdata = userdata[0][0]
    # else:
    #     print("查询缓存")
    #     userdata = ()
    #     for k in r.scan_iter('wx_user*'):
    #         verdata = r.hmget(k,'phone','email','password')
    #         if userphone == (verdata[0] or verdata[1]) and pwd == verdata[2]:
    #             userdata = r.hmget(k,'name')
    data = json.dumps(userdata)
    verify_code = session.get('imageCode')
    print(verify_code)
    if code != verify_code.lower():
        return ("0")
    if len(data) < 5:
        return ("1")
    else:
        json_list = []
        json_list.append(ran_char)
        json_list.append(userdata[0][0])
        username = json.dumps(json_list)
        # if not remem_me is None:
        r.setex(ran_char,604800,userdata[0][0])
        return username

#自动登录（修改过）
@userapp.route('/check_users/', methods=['POST', 'GET'], strict_slashes=False)
def check_users():
    userid = request.form.get('userid')
    if r.get(userid) == None:
        return ("1")
    else:
        username = r.get(userid)
        return ("2")


#退出删除redis（修改过）
@userapp.route('/clearkey/', methods=['POST', 'GET'], strict_slashes=False)
def clearkey():
    userid = request.form.get('userid')
    r.delete(userid)
    return ''
  
#网页修改密码(缓存，修改过)
@userapp.route('/change_passwords/', methods=['POST', 'GET'], strict_slashes=False)
def change_passwords():
    userid = request.form.get('userID')
    oldpwd = request.form.get('oldpwd')
    newpwd= request.form.get('newpwd')
    # mailcode = request.form.get('mailcode')
    # usermail = request.form.get('userMail') #用户接收验证码的邮箱
    # codeKey = ""+ usermail +":code"
    # code = r.get(codeKey)
    # if mailcode =='%s' % code:
    user_name = r.get(userid)
    user = wx_user.query.filter(wx_user.password == oldpwd and wx_user.name == user_name).first()
    if user:
        if len(r.keys('wx_user*')) != 0:
            for k in r.scan_iter('wx_user*'):
                r_username = r.hget(k,'name')
                if user_name == r_username:
                    user_infor = {'password':newpwd}
                    r.hmset(k,user_infor)
                    break
        user_update = wx_user.query.filter(wx_user.password == oldpwd and wx_user.name == user_name).update({'password': newpwd})
        db.session.commit()
        
        return("0")
    else:
        return("1")  


#网页修改手机号(缓存，修改过)
@userapp.route('/change_phones/', methods=['POST', 'GET'], strict_slashes=False)
def change_phones():
    userid = request.form.get('userID')
    # oldPhone = request.form.get('oldPhone')
    newPhone = request.form.get('newPhone')
    mailcode = request.form.get('mailcode')
    usermail = request.form.get('userMail') #用户接收验证码的邮箱
    codeKey = ""+ usermail +":code"
    code = r.get(codeKey)
    if mailcode =='%s' % code:
        
        if len(r.keys('wx_user*')) != 0:
            for k in r.scan_iter('wx_user*'):
                r_username = r.hget(k,'name')
                if r.get(userid) == r_username:
                    user_infor = {'phone':newPhone}
                    r.hmset(k,user_infor)
                    break
        sql = 'update wx_user set phone="'+newPhone+'" where name="'+r.get(userid)+'"'
        cursor.execute(sql)
        database.commit()
        
        return("0")
    else:
        return("1")    

#网页修改邮箱(缓存，修改过)
@userapp.route('/change_emails/', methods=['POST', 'GET'], strict_slashes=False)
def change_emails():
    user_id = request.form.get('userID')
    new_mail = request.form.get('newMail')
    mail_code = request.form.get('mailcode') #用户输入的验证码
    user_mail = request.form.get('oldMail') #用户接收验证码的邮箱
    codeKey = ""+ user_mail +":code"
    code = r.get(codeKey)
    if mail_code =='%s' % code:
        
        if len(r.keys('wx_user*')) != 0:
            for k in r.scan_iter('wx_user*'):
                r_username = r.hget(k,'name')
                if r.get(user_id) == r_username:
                    user_infor = {'email':new_mail}
                    r.hmset(k,user_infor)
                    break
        user = wx_user.query.filter(wx_user.email == user_mail).update({'email': new_mail})
        db.session.commit()
       
        return("0")
    else:
        return("1")    


# 网页端用户注册（修改过）
@userapp.route('/register/<user_name>', methods=['GET', 'POST'],strict_slashes=False)
def web_register(user_name):
    print(user_name)
    username = request.form.get('userName')
    pwd = request.form.get('pwd')
    userphone = request.form.get("userPhone")
    usermail = request.form.get("userMail")
    mailcode = request.form.get('mailCode')
    codeKey = ""+ usermail +":code"
    code = r.get(codeKey)
    user = wx_user.query.filter(wx_user.name == username or wx_user.phone == userphone).first()
    #找到
    if user:
        return ("2")
    else:
        # 判断邮箱验证码是否正确
        if mailcode == '%s' %code:
            for k in r.scan_iter('wx_user*'):
                r.delete(k)
            webuser = wx_user(name=username,email=usermail,phone=userphone,password=pwd,
                wx_id = 1,info_number = 0)
            db.session.add(webuser)
            db.session.commit()
            for k in r.scan_iter('wx_user*'):
                r.delete(k)
            return ("1")             
        else:
            return ("0")



# #网页端验证注册用户是否已经存在
# @userapp.route('/check_register/', methods=['GET', 'POST'])
# def check_register():
#     username = request.args.get("userName")
#     user = wx_user.query.filter(wx_user.name == username).first()
#     #找到
#     if user:
#         return ("1")
#     else:
#         return ("0")

# 网页获取个人中心数据(修改过)
@userapp.route('/getuserval/', methods=['GET', 'POST'])
def getuserval():
    userid = request.args.get('userID')
    userData = srch_hash_data('wx_user','name',r.get(userid))
    return userData

# 新——数据导出获取用户数据(导出数据要添加最上面的标题)
@userapp.route('/get_userdata/', methods=['GET', 'POST'])
def get_userdata():
    if len(r.keys('wx_user*')) == 0:
        sql='select * from wx_user'
        cursor.execute(sql)
        user_data=cursor.fetchall()
        fields = cursor.description
        column_list = []
        json_list = []
        for i in fields:
            column_list.append(i[0])
        for row in user_data:
            data = {}
            for i in range(len(column_list)):
                data[column_list[i]] = row[i]
            json_list.append(data)
            userData = json.dumps(json_list,ensure_ascii=False,cls=CJsonEncoder)
        for i in range(len(user_data)):
            user_infor = {'id':user_data[i][0],'name':user_data[i][1],'phone':user_data[i][2],'email':user_data[i][3],
                'password':user_data[i][4],'wx_id':user_data[i][5]}
            r.hmset('wx_user:%d'%(user_data[i][0]),user_infor)
            r.expire('wx_user:%d'%(user_data[i][0]),86400)
        return userData
    else:
        userdata = []
        for k in r.scan_iter('wx_user*'):
            data = r.hgetall(k)
            userdata.append(data)
        userdata = tuple(userdata)
        userdata = json.dumps(userdata,ensure_ascii=False,cls=CJsonEncoder)
        return userdata

