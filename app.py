from flask import Flask, render_template, redirect, url_for, request, make_response
import requests
import json

app = Flask(__name__)
HOST = 'http://127.0.0.1:5000'


def logged_in(func):
    def wrapper(*args, **kwargs):
        headers = {
            'Authorization': f'Bearer {request.cookies.get("token")}'
        }

        response = requests.request("POST", HOST + "/get_user_info", headers=headers)
        if response.status_code == 200:
            username = response.json()['username']
            return func(*args, **kwargs, logged_in=True, user=username)
        else:
            return func(*args, **kwargs, logged_in=False)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/")
@logged_in
def home(**kwargs):
    return render_template("index.html", **kwargs)


@app.route("/page2")
@logged_in
def page2(**kwargs):
    return render_template("page2.html", **kwargs)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", HOST + "/login", headers=headers, data=payload)

        if response.status_code == 200:
            token = response.json()['token']
            resp = make_response(redirect("/userportal"))
            resp.set_cookie('token', token)
            return resp
        return render_template("login.html", message=response.json()['message'])

    return render_template("login.html")


@app.route("/userportal")
@logged_in
def userportal(**kwargs):
    return render_template("userportal.html", **kwargs)


@app.route("/logout")
def logout():
    resp = make_response(redirect("/userportal"))
    resp.set_cookie('token', '', expires=0)
    return resp


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        confirm_password = request.values.get('confirm_password')
        if password != confirm_password:
            return render_template("register.html", message="Passwords not matching")
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", HOST + "/register", headers=headers, data=payload)

        if response.status_code == 200:
            token = response.json()['token']
            resp = make_response(redirect("/userportal"))
            resp.set_cookie('token', token)
            return resp
        return render_template("register.html", message=response.json()['message'])
    return render_template("register.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5888)
