#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import render_template

app = Flask(__name__)

# FRONTEND CODE

html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We"
      crossorigin="anonymous"
    />
    <script
      src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"
      integrity="sha384-eMNCOe7tC1doHpGoWe/6oMVemdAVTMs2xqW4mwXrXsW0L84Iytr2wi5v2QjrP/xp"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.min.js"
      integrity="sha384-cn7l7gDp0eyniUwwAZgrzD06kc/tftFf19TOAs2zVinnD/C7E91j9yyk5//jjpt/"
      crossorigin="anonymous"
    ></script>
    <meta charset="UTF-8" />
    <style>
      body {
        background-color: rgb(48, 50, 129);
        text-align: center;
        color: white;
        font-family: Arial, Helvetica, sans-serif;
      }
      form {
        display: flex;
        margin: 1rem;
      }

      .form {
        display: flex;
        flex-direction: column;
        max-width: 300pt;
        margin: auto;
      }

      .formViewiewContainer {
        display: flex;
        max-width: 900pt;
        margin: auto;
      }

      .viewData {
        border-radius: 4pt;
        background: #80808087;
        width: 200pt;
        margin-left: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      #companyPicture {
        width: 500px;
        border-radius: 10pt;
        margin: auto;
      }
    </style>
  </head>
  <body>
    <h1>🐍Python Coin Exchange🐍</h1>
    <p>Coin for your Cash!</p>
    <img
      src="https://listatoken.com/wp-content/uploads/2018/10/cryptocurrency-aleh-tsyvinski-ynews.jpeg"
      alt="Avatar"
      id="companyPicture"
    />

    <form action="/login" method="POST">
      <div class="formViewiewContainer">
        <div class="form">
          <label for="coin">Symbol of coin:</label>
          <div class="input-group mb-1">
            <input
              id="coin"
              type="text"
              class="form-control"
              placeholder="BTC, ETH, CEL ..."
              aria-label="Recipient's username"
              aria-describedby="button-addon2"
            />
            <button
              class="btn btn-outline-secondary"
              type="button"
              id="button-addon2"
              onclick="{getCoinData()}"
            >
              Check
            </button>
          </div>
          <label for="cash">Amount to purchase (USD):</label>
          <div class="input-group mb-1">
            <input
              id="cash"
              type="number"
              class="form-control"
              placeholder=""
              aria-label="Recipient's username"
              aria-describedby="button-addon2"
            />
          </div>
        </div>
        <div id="coinContainer" class="viewData">
          <div id="coinName" name="coinname"></div>
          <div id="coinPrice" name="price"></div>
          <div id="howMuch" name="qty"></div>
        </div>
      </div>
    </form>
    <button class="btn btn-secondary" type="button" id="button-addon2">
      Submit to the dashboard
    </button>
  </body>
  <script typt="text/javascript">
    // it's dupe I get it
    var toggleBtn = false;
    var price = null;
    var $coinName = document.getElementById("coinName");
    var $coinPrice = document.getElementById("coinPrice");
    var $howMuchCoin = document.getElementById("howMuch");
    async function getCoinData() {
      toggleBtn = true;
      //if I have enough time make the display appear dynamically
      // var newDiv = document.createElement("div");
      var symbol = document.getElementById("coin").value;
      const response = await fetch(
        "https://cors-access-allow.herokuapp.com/https://api.lunarcrush.com/v2?data=assets&key=nj74pb5ijzpw1l3y01zb28&symbol=" +
          symbol,
        {
          method: "GET", // *GET, POST, PUT, DELETE, etc.
          mode: "cors", // no-cors, *cors, same-origin
          cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
          credentials: "same-origin", // include, *same-origin, omit
          headers: {
            "Content-Type": "application/json",
          },
        },
      )
        .then((resp) => resp.json())
        .then((data) => {
          $coinName.innerText = data.data[0].name;
          $coinPrice.innerText = data.data[0].price + " (USD)";
          price = data.data[0].price;
        });
    }

    const calcCoin = (e) => {
      //band-aid because checking the input vlaue was wishy washy
      if (e.target.value !== "") {
        if (toggleBtn) {
          //Fill element to show our value
          var calcQ = e.target.value / price;
          $howMuchCoin.innerText =
            "You can purchase " + calcQ + " " + $coinName.innerText;
        } else {
          alert("Please select a crypto first please. Thank you.");
          $inputUSD.value = "";
        }
      } else {
        $howMuchCoin.innerHTML = "";
      }
    };
    var $inputUSD = document.getElementById("cash");
    $inputUSD.addEventListener("input", calcCoin);
  </script>
</html>
"""
j2 = """"{% for host in groups %}
   <h4><span>{{ host.ip }}   {{ host.fqdn }} # {{ host.hostname }}</span></h4>
   {% endfor %}

<br>
<li><a href = '/form'></b>Click here to add more data</b></a></li>
<li><a href = '/logout'></b>Click here to log out</b></a></li>
"""

coins = [{"coinname": "BTC", "price": "56", "qty": "4"}]

# BACKEND CODE


@app.route("/correct")
def success():
    return f"That is correct!"


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
    return render_template(j2, coins=coins)


@app.route("/login", methods=["GET", "POST"])
def login():
    # HTML form that collects hostname, ip, and fqdn values
    if request.method == "POST":
        session["username"] = request.form.get("username")
    if "username" in session and session["username"] == "admin":
        return html
    # # Just testing out abort so I type abort as username
    # if "username" in session and session["username"] == "abort":
    #     abort(401)
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
