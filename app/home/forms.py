from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# 登录表单页面
class LoginForm(FlaskForm):
    '''用户登录表单'''
    # 账号
    username = StringField(
        label='用户名',  # 标签
        validators=[
            DataRequired("请输入账号！")
        ],
        description="用户名",
        render_kw={
            "class": "form-control",
            "id": "inputEmail3",
            "placeholder": "username"
        }
    )

    # 密码
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired('请输入密码！')
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "id": "inputPassword3",
            "placeholder": "Password"
        }
    )
    # 提交
    submit = SubmitField(
        label='注册',
        render_kw={
            "class": "btn btn-default",
            "value": "登录"
        }
    )

# 注册表单页面
class RegisterForm(FlaskForm):
    '''用户注册表单'''
    # 账号
    username = StringField(
        label='用户名',  # 标签
        validators=[
            DataRequired("请输入账号！")
        ],
        description="用户名",
        render_kw={
            "id": "username",
            "class": "form-control",
            "placeholder": "请输入用户名",
            "maxlength": "20"
        }
    )

    # 密码
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired('请输入密码！')
        ],
        description="密码",
        render_kw={
            "id": "password",
            "class": "form-control",
            "placeholder": "请输入密码",
            "maxlength": "20"
        }
    )
    # 提交
    submit = SubmitField(
        label='注册',
        render_kw={
            "class": "form-control btn btn-primary",
            "id": "submit",
            "value": "立即注册"
        }
    )