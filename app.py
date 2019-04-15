from flask import Flask, render_template

app = Flask(__name__)


# 主页
@app.route('/')
def home():
    return render_template("home/index.html")


# 图像
@app.route('/image')
def face():
    return render_template("home/blog.html")


if __name__ == "__main__":
    app.run(debug=True)
