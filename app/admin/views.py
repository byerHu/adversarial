# coding:utf8
from . import admin  # 从当前目录导入admin蓝图


@admin.route("/")
def index():
    return "<h1 style='color:red;'>this is admin</h1>"