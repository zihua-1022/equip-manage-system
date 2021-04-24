# 导入表单基类
from flask_wtf import FlaskForm
# 导入相关字段
from wtforms import StringField,PasswordField,SubmitField,BooleanField
# 导入相关验证器类
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    account=StringField('账号',validators=[DataRequired('请输入账户')])
    password=PasswordField('密码',validators=[DataRequired('请输入密码')])
    imageCode=StringField('验证码',validators=[DataRequired('请输入验证码')])
    remember = BooleanField('记住我')
    submit=SubmitField('登录')