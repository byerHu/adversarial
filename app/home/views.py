# coding:utf8
from . import home  # 从当前目录导入home蓝图
from flask import render_template, request, flash, redirect, url_for, session
from app.home.forms import LoginForm, RegisterForm
from app import app
from app.models import User
from app import db, app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_
import json
import os
from keras.models import load_model
import numpy as np
from PIL import Image
import cv2
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class

# 文件上传
photos = UploadSet('photos', IMAGES)
# 设置上传文件的地址
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads/'
# 上传的初始化
configure_uploads(app, photos)
# 配置上传文件大小，默认64M,设置None则会采用MAX_CONTENT_LENGTH配置选项
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
patch_request_class(app, size=None)



# 首页
@home.route("/")
def index():
    return render_template('home/index.html')

# 登录页
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            flash("用户不存在！", "err1")
        elif data['pwd'] != user.pwd:
            flash("密码错误!", "err2")
        else:
            login_user(user)
            # 登录成功,保存会话
            session[user.username] = data['username']
            return redirect(url_for('home.index'))

    return render_template('home/login.html', form=form)
# 登出
@home.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆')
    return redirect(url_for('home.login'))

# 注册页
@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        # print(data)
        user = User.query.filter_by(username=data["username"]).first()
        if user:
            flash("用户名已经注册!", "err")
            return redirect(url_for('home.register'))
        user = User(
            username=data["username"],
            pwd=data["pwd"]
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功,请登录", "ok")
        return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)

# 图像
@app.route('/cvFace')
def cvFace():
    return render_template("home/cv.html")


# 上传文件
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    img_url = None
    if request.method == 'POST' and 'photo' in request.files:
        # 生成随机的文件名
        suffix = os.path.splitext(request.files['photo'].filename)[1]
        filename = os.path.splitext(request.files['photo'].filename)[0] + suffix
        # 保存上传文件
        photos.save(request.files['photo'], name=filename)
        # 生成缩略图
        pathname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 1.打开文件
        img = Image.open(pathname)
        # 2.设置尺寸
        img.thumbnail((128, 128))
        # 3.保存修改后的文件
        img.save(pathname)
        # 获取上传文件的URL
        img_url = photos.url(filename)
        return render_template('home/cv.html', img_url=img_url)

from keras.datasets import mnist

model = load_model('../model/mnist/mnist_h5')
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 图像识别
@app.route('/recognition')
def recognition():
    data = request.args.get('filename')
    src = cv2.imread('./uploads/'+data)
    print(data)
    # 将图片转化成28*28的灰度图
    src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    dst = cv2.resize(src,(28,28),interpolation=cv2.INTER_CUBIC)

    # 将灰度图转化成1*784的能够输入网络的数组
    picture = np.zeros((28,28))
    for i in range(0,28):
        for j in range(0,28):
            picture[i][j] = (255 - dst[i][j])
    picture = picture.reshape(1,28,28,1)




    predict_2 = model.predict(picture.reshape(1, 784))
    print(np.argmax(predict_2[0]))
    print(predict_2)

    return render_template('home/cv.html')

# 图像
@app.route('/login')
def login():
    return render_template("home/login.html")
