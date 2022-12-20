from flask import *
import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
from flask import Blueprint
import jwt
from flask import make_response
import requests
import datetime
import re

order = Blueprint("order", __name__)

dbconfig = {
    "host": "localhost",
    "database": "taipei_day_trip",
    "user": "root",
    "passwd": "",
    "charset": "utf8mb4", "auth_plugin": 'mysql_native_password'}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=32, **dbconfig)


@order.route("/api/orders", methods=["POST"])
def orders():
    framework = request.cookies.get("token")
    token_decode = jwt.decode(
        framework, "secret", algorithms=["HS256"])
    id = int(token_decode["id"])

    data = request.get_data()
    data_read = json.loads(data)

    prime = data_read["prime"]
    merchant_id = ""
    customer_phone_number = data_read["order"]["contact"]["phone"]
    customer_name = data_read["order"]["contact"]["name"]
    customer_email = data_read["order"]["contact"]["email"]
    price = data_read["order"]["price"]

    date = f"{datetime.datetime.today()}"
    only_int_date = re.findall(r"\d+", date)
    order_number = "".join(only_int_date)

    copy_from_booking = "INSERT INTO orders(id,attractionId,date,time,price) SELECT id,attractionId,date,time,price FROM booking WHERE id = %s;"
    update_order_number = "UPDATE orders SET orderNumber = %s,phone = %s,paid='未付款' where id = %s;"

    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()

    try:
        cursor.execute(copy_from_booking, (id,))
        cnx.commit()
        cursor.execute(update_order_number,
                       (order_number, customer_phone_number, id))
        cnx.commit()

        api_endpoint = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": ""
        }

        payload = {
            "prime": prime,
            "partner_key": "",
            "merchant_id": merchant_id,
            "details": "TapPay Test",
            "amount": price,
            "order_number": order_number,
            "currency": "TWD",
            "cardholder": {
                "phone_number": customer_phone_number,
                "name": customer_name,
                "email": customer_email,
                "zip_code": "",
                "address": "",
                "national_id": ""
            },
            "remember": False
        }

        response = requests.post(api_endpoint, json=payload, headers=headers)

        if response.status_code == 200:

            update_paid = "UPDATE orders SET paid='已付款' WHERE orderNumber = %s;"
            delete_booking_data = "DELETE FROM booking WHERE id = %s"

            try:
                cursor.execute(update_paid, (order_number,))
                cnx.commit()
                cursor.execute(delete_booking_data, (id,))
                cnx.commit()

                pay_success = {
                    "data": {
                        "number": order_number,
                        "payment": {
                            "status": 0,
                            "message": "付款成功"
                        }
                    }
                }
                return pay_success

            except Error as e:
                print(e)
                error = {
                    "error": True,
                    "message": "資料庫更新錯誤"
                }
                return error

        else:

            print("Error:", response.status_code)
            pay_failed = {
                "error": True,
                "message": "付款失敗"
            }
            return pay_failed
    except Error as e:
        print(e)
        error = {
            "error": True,
            "message": "資料庫錯誤"
        }
        return error
