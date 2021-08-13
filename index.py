#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import render_template
# added abort
from flask import abort

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

app = Flask(__name__)

# Load all the HTML/CSS here. Had issues with
# html = """<style>
# body {
#   background-color: black;
#   text-align: center;
#   color: white;
#   font-family: Arial, Helvetica, sans-serif;
# }
# </style>
# </head>
# <body>

# <h1>TRIVIA TIME</h1>
# <p>What is the meaning of life, the universe, and everything?</p>
# <img src="https://stevetobak.com/wp-content/uploads/2021/02/dont-panic.png" alt="Avatar" style="width:200px">

#     <form action = "/login" method = "POST">
#         <p><input type = "text" name = "nm"></p>
#         <p><input type = "submit" value = "submit"></p>
#     </form>

# </body>

# </html>"""

# Add my api secret key
# secret key wooooo

coins = [{"coinname": "BTC", "price": "56", "qty": "4"}]


# This will be used to grab the lastest price on load
# def getTop():
#   url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#   parameters = {
#     'start':'1',
#     'limit':'10',
#     'convert':'USD'
#   }
#   headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': '8d15a1f1-acc7-4cbd-b4f7-914159627381',
#   }

#   session = Session()
#   session.headers.update(headers)

#   try:
#     response = session.get(url, params=parameters)
#     data = json.loads(response.text)
#     print(data)
#   except (ConnectionError, Timeout, TooManyRedirects) as e:
#     print(e)
# getTop()


# @app.route("/correct")
# def success():
#     return f"That is correct!"


# @app.route("/")
# def start():
#     return html

@app.route("/logout")
def logout():
    # accessing this page pops the value of username of the session
    session.pop("username", None)
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def hosts():
    # GET returns the rendered hosts
    # POST adds new hosts, then returns rendered hosts
    if "username" in session and session["username"] == "admin":
        if request.method == "POST":
            # pull all values from posted form
            name = request.form.get("coinname")
            price = request.form.get("price")
            qty = request.form.get("qty")
            # create a new dictionary with values, add to coins
            coins.append({"name": name, "price": price, "qty": qty})
    return render_template("coinpurchased.j2", coins=coins)


@app.route("/login", methods=["GET", "POST"])
def login():
    # HTML form that collects hostname, ip, and fqdn values
    if request.method == "POST":
        session["username"] = request.form.get("username")
    if "username" in session and session["username"] == "admin":
        return render_template("coinrequestform.html.j2")
    # Just testing out abort so I type abort as username
    if "username" in session and session["username"] == "abort":
        abort(401)
    else:
        return """
     <form action = "" method = "post">
        <p>Invalid Login.</p>
        <p><input type = text name = username></p>
        <p><input type = submit value = Login></p>
     </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224)  # runs the application
