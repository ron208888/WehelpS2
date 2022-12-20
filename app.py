from flask import *
import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
from flask_cors import CORS
from flask import Blueprint
from attraction import attraction
from user import user

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(attraction)
app.register_blueprint(user)

# Pages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
