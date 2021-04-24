from common.exts import db
from datetime import datetime
from flask_login import UserMixin

class webuser(UserMixin,db.Model):
    __tablename__='webuser'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    account=db.Column(db.String(12),nullable=False)
    password=db.Column(db.String(12),nullable=False)
    phone=db.Column(db.String(11),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    

class wx_user(db.Model):
    __tablename__='wx_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(200),nullable=False)
    phone=db.Column(db.String(11),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    wx_id=db.Column(db.String(25),nullable=False)
    info_number=db.Column(db.Integer,nullable=False)
    control_power = db.Column(db.Integer, nullable=False)
    
class upload_img(db.Model):
    __tablename__='upload_img'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,nullable=False)
    number=db.Column(db.Integer,nullable=False)
    # """
    # datetime.now()获取的是服务器第一次运行的时间，以后每次的添加数据的时间都相同
    # datetime.now每次创建模型的时候都会获取当前时间，即添加数据的时候获取添加数据的的当前时间，每次不相同
    # """
    date=db.Column(db.DateTime,default=datetime.now)
    imgs=db.relationship('imgs',backref='upload')
    equip_id=db.Column(db.Integer,nullable=False)
    image_desc=db.Column(db.String(255),nullable=False)
    image_title=db.Column(db.String(30),nullable=False)

class imgs(db.Model):
    __tablename__='imgs'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    upload_id=db.Column(db.Integer,db.ForeignKey('upload_img.id'))
    file_path=db.Column(db.String(300),nullable=False)
    data_path=db.Column(db.String(300),nullable=False)

class information(db.Model):
    __tablename__='information'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,nullable=False)
    image_id=db.Column(db.Integer,nullable=False)
    equip_id=db.Column(db.Integer,nullable=False)

class equipment(db.Model):
    __tablename__='equipment'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    equip_name=db.Column(db.String(30),nullable=False)
    equip_disc=db.Column(db.String(255),nullable=False)
    if_work=db.Column(db.Integer,nullable=False)
    equip_adr=db.Column(db.String(50),nullable=False)
    equip_ip=db.Column(db.String(30),nullable=False)
    equip_posi=db.Column(db.String(50),nullable=False)
    equip_image=db.Column(db.String(50),nullable=False)
    equip_code=db.Column(db.String(30),nullable=False)


class logs(db.Model):
    __tablename__='logs'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(12),nullable=False)
    user_type=db.Column(db.String(12),nullable=False)
    phone=db.Column(db.String(11),nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    logs_typeid=db.Column(db.Integer,nullable=False)
    beinfo=db.Column(db.String(255),nullable=False)
    afinfo=db.Column(db.String(255),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now)


class logs_type(db.Model):
    __tablename__='logs_type'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
    logs_typename=db.Column(db.String(12),nullable=False)