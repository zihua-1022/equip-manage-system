from gevent import monkey
monkey.patch_all()
from flask import Flask,make_response,session,render_template
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sockets import Sockets
from flask_mail import Mail
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from datetime import timedelta
from common import config
from model.models import webuser,upload_img,information,equipment
from common.exts import db
from controller.user import getOpenid
from io import BytesIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from controller.dataProcess import ReciveData
from controller.autoTranData import autoReciveData
from controller.scanQrcode import startEquip
import gvcode
import threading,time
from captcha.image import ImageCaptcha
from random import randint


app = Flask(__name__)
app.config.from_object(config)
sockets = Sockets(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'  # 对话保护等级
login_manager.login_view = 'login'  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 设置快闪消息，定义需要登录访问页面的提示消息
login_manager.remember_cookie_duration = timedelta(days=7)  # 设置 cookie 的有效期，默认1年

db.init_app(app)
# 创建邮箱类实例
mail = Mail(app)

# 保存用户的设备的自动传输脚本在线的标识
equip_dict = {
    # 'nick_name': 'webSocket_obj'
}


# 发送邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# user_loader 回调函数,作用就是通过 id 返回对应的 User 对象。
@login_manager.user_loader
def load_user(id):
    return webuser.query.filter(webuser.id == id).first()

# 微信绑定邮箱发送验证码（需增加）
@app.route('/wx_bindemail/', methods=['POST'])
def wx_bindemail():
    code = "%06d" % random.randint(0, 999999)
    openid = request.values.get('openid')
    print(openid)
    user=wx_user.query.filter(wx_user.wx_id == openid).first()
    username=user.name
    usermail=request.values.get('bindmail')  
    codeKey = ""+ usermail +":code"
    r.setex(codeKey,120,code)#把code存进redis中,设置其60s过期时间
    try:
        msg = Message('fosu-验证邮件',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<h1>Hi，Friend</h1></br>以下6位数字是邮箱验证码，请在小程序上填写以通过验证,验证码将在2分钟后过期。\
        </br>您的验证码为<h2 style=" width: 66px;background: #6777ef; border-radius: 4px; padding: 6px 12px;font-family: Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; \
        font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;">%s</h2>' % code
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    except expression as identifier:
        print('发送失败')
    return ''

# 微信修改邮箱（新）和判断验证码
@app.route('/wx_update_mail/', methods=['POST'])
def wx_update_mail():
    openid=request.values.get('openid')
    newmail = request.form.get('newmail')
    mailcode = request.form.get('mailcode') 
    codeKey = ""+ newmail +":code"
    code = r.get(codeKey)
    isveri=request.form.get('isveri')
    if isveri:
        if mailcode =='%s' % code:
            return jsonify({'status':'success'}) 
        else:
            return jsonify({'status':'fail'}) 
    else:
        if mailcode =='%s' % code:
            sql = 'update wx_user set email="'+newmail+'" where wx_id="'+openid+'"'
            cursor.execute(sql)
            database.commit()
            return jsonify({'status':'success'}) 
        else:
            return jsonify({'status':'fail'}) 
        
#微信小程序修改密码
@app.route('/wx_update_password/', methods=['POST'])
def wx_update_password():
    password=request.values.get('password')
    openid=request.values.get('openid')
    sql = 'update wx_user set password="'+password+'" where wx_id="'+openid+'"'
    cursor.execute(sql)
    database.commit()
    return jsonify({'status':'success'}) 

# 注册和修改信息发送邮件验证码
@app.route('/sendcode/', methods=['POST'])
def sendcode():
    code = "%06d" % random.randint(0, 999999)
    usermail = request.form.get('userMail')
    codeKey = ""+ usermail +":code"
    r.setex(codeKey,120,code)#把code存进redis中,设置其60s过期时间
    try:
        msg = Message('设备信息化管理系统-验证邮件',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<h1>Hi，Friend</h1></br>以下6位数字是邮箱验证码，请在网站上填写以通过验证,验证码将在2分钟后过期。\
        </br>您的验证码为<h2 style=" width: 66px;background: #6777ef; border-radius: 4px; padding: 6px 12px;font-family: Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; \
        font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;">%s</h2>' % code
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    except expression as identifier:
        print('发送失败')
    return ''

#网页用户找回帐号密码(修改过)
@app.route('/findloss/', methods=['POST', 'GET'], strict_slashes=False)
def findloss():
    usermail = request.form.get('userMail')
    sql = 'select *from wx_user where email="' + usermail + '"'
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 0:
        print('发送失败')
        return ("0")
    else:
        msg = Message('帐号密码找回',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<b>您的帐号为%s，密码为%s<b>' %(data[0][1],data[0][4])
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    
        return ("1")  

#自动传输的时候接收客户端数据
@sockets.route('/Auto')
def auto_rec(ws):
    rec = autoReciveData(ws)
    rec.runThread()

#接收客户端数据
@sockets.route('/')
def tran_data(ws):
    rec = ReciveData(ws)
    rec.runThread()


##############以下为显微镜自动传输数据代码###############
#自动传输启动脚本
@sockets.route('/script/<content>/<code>')
def script(ws,content,code):
    equip_dict[code] = ws
    rec = startEquip(ws,code)
    rec.runThread()
# 每隔3分钟，客户端就向服务器发送一个心跳包；服务器收到以后，记录当前的收到该客户端心跳包的时间。
# 服务器有一个心跳检测线程，
# 当一个客户端连接连续9分钟没有收到心跳包，
# 则认为该连接已经断开了。   

# 手机扫码验证使用者页面
@app.route('/qrcode/<content>/<code>')
def scan_qrcode(content,code):
    return render_template('register.html')

@app.route('/write_exp_infor/<user_equip>')
def write_exp_infor(user_equip):
    return render_template('writeExpInfor.html')

#扫码自动传输数据处理
def upload_infor(user_id,theme,desc,code):
    equip = equipment.query.filter(equipment.equip_code == code).first()  # 获取刚刚上传图片数据的id
    equip_id = equip.id

    upload_data = upload_img(user_id=user_id, number=0,equip_id=equip_id,
        image_desc=desc, image_title=theme)  # 将当前登录用户的id作为upload_img的user_id
    db.session.add(upload_data)
    db.session.commit()

    upoload = upload_img.query.filter(
        upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
    image_id = upoload.id  # 获取当前上传用户的id


    sql='select id from wx_user'#查询所有用户的id
    cursor.execute(sql)#执行SQL语句
    alluser_id=cursor.fetchall()#获取所有用户的id

    # 使用for/in循环对所有用户添加未读数据
    for (i,) in alluser_id:
        info_data = information(user_id=i, image_id=image_id, equip_id=equip_id)  # 设备equip_id目前手动设置
        db.session.add(info_data)
        db.session.commit()

#验证使用自动传输的用户
@app.route('/user_verify', methods=['POST', 'GET'], strict_slashes=False)
def user_verify():
    userphone = request.form.get('userphone')
    pwd = request.form.get('password')
    remem_me = request.form.get('remember_me')
    phone_mail = '\'%s\'' % userphone
    password = '\'%s\'' % pwd
    sql = 'select id from wx_user where phone=%s and password=%s or email=%s and password=%s' %(phone_mail,password,phone_mail,password)
    cursor.execute(sql)
    user_id = cursor.fetchall()
    data = json.dumps(user_id)
    if len(data) < 5:
        return '0'
    else:
        return data

#小程序远程控制显微镜的脚本命令代码
@app.route('/upload_exp_infor/<start_type>',methods=['POST', 'GET'], strict_slashes=False)
def exp_infor(start_type):
    code = request.values.get('equipCode')
    theme = request.values.get('theme')
    desc = request.values.get('desc')
    user_id = request.values.get('userID') 
    for equip_code,e_socket in equip_dict.items():
        if code == equip_code:               
            if start_type == 'powerOn':  #打开程序和相机
                e_socket.send('Camera')    
                return '相机启动成功！'                       
            # elif start_type == 'takePho':  #开始采集
            elif start_type == 'takePho':
                user = wx_user.query.filter(wx_user.wx_id == user_id).first()
                if user:
                    d = upload_infor(user.id,'控制设备','小程序用户远程控制设备',code)
                    e_socket.send('Collect')
                    return '相机拍照中，稍后可查看结果！' 
            else:
                d = upload_infor(user_id,theme,desc,code)    
                e_socket.send('Online')
                return '机器已经启动！'           
            #上传数据upLoad
            break
    return '机器已离线！请稍后连接...'


# 获取登录的验证码（转小写有问题？）
@app.route('/get_imageCode/')
def get_imageCode():
    # 生成验证码图片
    image, code = gvcode.generate()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    # 将验证码字符串储存在session中
    session['imageCode'] = code
    return response

if __name__=='__main__':
    from controller.user import *
    from controller.image import *
    from controller.logs import *
    from controller.equipment import *
    from controller.fileOpera import *
    
    app.register_blueprint(userapp)    #注册蓝图文本
    app.register_blueprint(imageapp)
    app.register_blueprint(logsapp)
    app.register_blueprint(equipapp)
    app.register_blueprint(fileoperaapp)
    

    # 创建一个 websocket客户端，监听的地址0.0.0.0：80
    server = pywsgi.WSGIServer(('0.0.0.0',443), application=app, handler_class=WebSocketHandler)
    print('server started')
    # 开启websocket长连接，
    server.serve_forever()
