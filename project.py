#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import render_template

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# import win32api

app = Flask(__name__)

# Add my api secret key
app.secret_key = "superrandom key that nonone knows about"

coins = []

pricecollector = []
# coinmarketcap API
# This will be used to grab the lastest price on load


def getTop():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': '1',
        'limit': '300',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '8d15a1f1-acc7-4cbd-b4f7-914159627381',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def getDogeStory():
    url = 'https://api.lunarcrush.com/v2?'
    parameters = {
        'data': 'feeds',
        'key': 'nj74pb5ijzpw1l3y01zb28',
        'symbol': 'DOGE',
        'limit': 10,
        'sources': 'twitter'
    }
    headers = {
        'Accepts': 'application/json',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# def getTotal():
#     for c in coins:
#         collector = collector + (c['qty'] * c['price'])
#     if collector > 100000:
#         win32api.MessageBox(0, 'hello', 'title')


@app.route("/logout")
def logout():
    # pop the username off of the session
    session.pop("username", None)
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def hosts():
    topcoin = getTop()
    story = getDogeStory()
    print(story)
    # getTotal()   #TO DO look into win32 promts
    # GET call returns the 'cart'
    # POST call adds new purchased coins, then returns rendered 'cart'
    if "username" in session and session["username"] == "admin":
        if request.method == "POST":
            # pull all values from posted form
            name = request.form.get("coinname")
            price = request.form.get("price")
            qty = request.form.get("qty")
            # create a new dictionary with values, add to coins dict
            coins.append({"coinname": name, "price": price, "qty": qty})
    return render_template("coinpurchased.html.j2", coins=coins, topcoin=topcoin, story=story)


@app.route("/form", methods=["GET", "POST"])
def login():
    topcoin = getTop()
    story = getDogeStory()
    # html form that collects values
    if request.method == "POST":
        session["username"] = request.form.get("username")
    if "username" in session and session["username"] == "admin":
        return render_template("coinrequestform.html.j2", topcoin=topcoin)
    else:
        return render_template("loginform.html.j2", story=story)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224)  # runs the application
