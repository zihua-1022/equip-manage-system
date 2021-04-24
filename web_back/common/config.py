"""
整个程序的配置文件，所有全局配置属性在这里设置
"""
from datetime import timedelta

import os
# import redis

DEBUG=True
GEVENT_SUPPORT=True
SECRET_KEY=os.urandom(24)

# 数据库参数设置
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'wechat_demo'

SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT,DRIVER,USERNAME,
PASSWORD,HOST,PORT,DATABASE)
# SQLALCHEMY_DATABASE_URI="{}+{}://{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,HOST,PORT,DATABASE)


# flask-mail参数设置
MAIL_SERVER = 'smtp.qq.com'                #邮件服务器地址
MAIL_PORT = 465                           #邮件服务器端口
MAIL_USE_TLs = False
MAIL_USE_SSL = True                      #qq邮箱需要使用SSL
MAIL_USERNAME = '351053928@qq.com'         #填邮箱名
MAIL_PASSWORD = 'yijdjkrnciwqbiha'         #邮箱授权码
#  MAIL_PASSWORD = = os.environ.get('MAIL_PASSWORD'),#从系统中获取授权码
MAIL_DEBUG = True

SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1)

SQLALCHEMY_TRACK_MODIFICATIONS=True
SQLALCHEMY_COMMIT_TEARDOWN=True