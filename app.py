from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    args = request.args
    return render_template("index.html", name=args.get("name"), city="Sofia")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
