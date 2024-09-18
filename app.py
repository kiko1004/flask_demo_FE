from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    args = request.args
    return render_template("index.html")

@app.route("/page2")
def page2():
    return render_template("page2.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5888)
