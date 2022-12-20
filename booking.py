from flask import *
import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
from flask import Blueprint
import jwt
from flask import make_response

booking = Blueprint("booking", __name__)

dbconfig = {
    "host": "localhost",
    "database": "taipei_day_trip",
    "user": "root",
    "passwd": "12345678",
    "charset": "utf8mb4", "auth_plugin": 'mysql_native_password'}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=32, **dbconfig)


def set_img(data_dict):
    count = 0
    img = {}
    for i in data_dict:
        count += 1
        format = i["images"].split("https")
        img[count] = []
        for j in format:
            if j != "":
                img[count].append(f"https{j}")
    count = 0
    for k in data_dict:
        count += 1
        k["images"] = img[count]
    return data_dict


@booking.route("/api/booking", methods=["GET", "POST", "DELETE"])
def doBooking():
    framework = request.cookies.get("token")
    token_decode = jwt.decode(
        framework, "secret", algorithms=["HS256"])
    id = int(token_decode["id"])
    userName = token_decode["name"]
    email = token_decode["email"]

    if request.method == "GET":
        info = {}
        error = {"error": True}
        unpaid = "SELECT * FROM booking WHERE id = %s"
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        try:
            cursor.execute(unpaid, (id,))
            result = cursor.fetchall()

            if result == []:
                info["data"] = {"error": True,
                                "userName": userName, "email": email}
                return jsonify(info)

            column = [index[0] for index in cursor.description]
            data_dict = [dict(zip(column, row))
                         for row in result]

            info["data"] = []

            for i in data_dict:
                try:
                    attraction = "SELECT * FROM attractions WHERE id = %s"
                    cursor.execute(attraction, (i["attractionId"],))
                    attraction_result = cursor.fetchall()

                    column = [index[0] for index in cursor.description]
                    attraction_dict = [dict(zip(column, row))
                                       for row in attraction_result]
                    set_img(attraction_dict)

                    bookingInfo = {"attraction": {
                        "id": attraction_dict[0]["id"],
                        "name": attraction_dict[0]["name"],
                        "address": attraction_dict[0]["address"],
                        "image": attraction_dict[0]["images"][0],
                    },
                        "date": i["date"],
                        "time": i["time"],
                        "price": i["price"],
                        "userName": userName,
                        "email": email}

                    info["data"].append(bookingInfo)

                except Error as e:
                    print(e)
                    return jsonify(error)

            return jsonify(info)

        except Error as e:
            print(e)
            return jsonify(error)

        finally:
            cursor.close()

    elif request.method == "POST":

        data = request.get_data()
        data_read = json.loads(data)

        attractionId = data_read["attractionId"]
        date = data_read["date"]
        time = data_read["time"]
        price = data_read["price"]
        success = {}
        error = {"error": True}

        checkTime = "SELECT date,time FROM booking WHERE id = %s;"
        bookingInsert = "INSERT INTO booking(id,attractionId,date,time,price) VALUES(%s,%s,%s,%s,%s);"
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        try:
            cursor.execute(checkTime, (id,))
            result = cursor.fetchall()

            try:

                column = [index[0] for index in cursor.description]
                data_dict = [dict(zip(column, row))
                             for row in result]

                if data_dict == []:
                    cursor.execute(
                        bookingInsert, (id, attractionId, date, time, price))
                    cnx.commit()
                    success = {"ok": True}

                    return jsonify(success)

                for i in data_dict:

                    if i["date"] == date and i["time"] == time:
                        error["message"] = "SameTime"
                        return jsonify(error)

                cursor.execute(
                    bookingInsert, (id, attractionId, date, time, price))
                cnx.commit()
                success = {"ok": True}

                return jsonify(success)

            except Error as e:
                print(e)
                error["message"] = "伺服器錯誤"
                return jsonify(error)

            finally:
                cursor.close()

        except Error as e:
            print(e)
            error["message"] = "伺服器錯誤"
            return jsonify(error)

        finally:
            cursor.close()

    elif request.method == "DELETE":
        data = request.get_data()
        data_read = json.loads(data)

        date = data_read["date"]
        time = data_read["time"]
        success = {"ok": True}
        error = {"error": True}

        delete = "DELETE FROM booking WHERE id=%s AND date=%s AND time=%s;"
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        try:
            cursor.execute(delete, (id, date, time))
            cnx.commit()

            return jsonify(success)

        except Error as e:
            print(e)
            error["message"] = "伺服器錯誤"
            return jsonify(error)

        finally:
            cursor.close()
