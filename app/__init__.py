# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import LoginManager

app = Flask(__name__)

# 连接test数据库
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'b26273f62a0d44568360ee8570221c24'
app.debug = True
# 实例化数据库对象
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.login'

from app.home import home as home_blueprint  # 导入home蓝图对象
from app.admin import admin as admin_blueprint  # 导入admin蓝图对象

app.register_blueprint(home_blueprint)  # 注册home蓝图
app.register_blueprint(admin_blueprint, url_prefix="/admin")  # 注册admin蓝图对象