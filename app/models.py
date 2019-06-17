# coding:utf8
from datetime import datetime

from app import db

from flask_login import UserMixin
from app import login_manager


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))


# 用户数据模型
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    username = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码

