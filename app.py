from flask import Flask, render_template, request
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class
import os
from PIL import Image
import keras
from keras.models import load_model
import numpy as np
from PIL import Image
import cv2

app = Flask(__name__)

# 文件上传
photos = UploadSet('photos', IMAGES)
# 设置上传文件的地址
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads/'
# 上传的初始化
configure_uploads(app, photos)
# 配置上传文件大小，默认64M,设置None则会采用MAX_CONTENT_LENGTH配置选项
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
patch_request_class(app, size=None)


# 主页
@app.route('/')
def home():
    return render_template("home/index.html")


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

model = load_model('./models/mnist/mnist_h5')
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

if __name__ == "__main__":
    app.run(debug=True)
