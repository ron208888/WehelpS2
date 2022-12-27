import os
from dotenv import load_dotenv
from flask import *
import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
from flask import Blueprint
import jwt
from flask import make_response

user = Blueprint("user", __name__)
load_dotenv()

dbconfig = {
    "host": "localhost",
    "database": "taipei_day_trip",
    "user": "root",
    "passwd": os.getenv("db_password"),
    "charset": "utf8mb4", "auth_plugin": 'mysql_native_password'}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=3, **dbconfig)


@user.route("/api/user", methods=["POST"])
def sign_up():
    data = request.get_data()
    data_read = json.loads(data)

    sign_up_success = {"ok": True}
    error = {"error": True}

    name = data_read["name"]
    email = data_read["email"]
    password = data_read["password"]

    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()

    try:
        sign_up = "INSERT INTO member(name,email,password) VALUES(%s,%s,%s)"
        cursor.execute(sign_up, (name, email, password))
        cnx.commit()
        return jsonify(sign_up_success)

    except Error as e:
        print(e)

        error["message"] = "此信箱已註冊"
        return jsonify(error)

    finally:
        cnx.close()


@user.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def sign_in():
    sign_in_success = {"ok": True}
    error = {"error": True}

    if request.method == "GET":
        framework = request.cookies.get("token")
        member_data = {}

        if framework == None:
            member_data["data"] = None
            return jsonify(member_data)

        try:
            token_decode = jwt.decode(
                framework, "secret", algorithms=["HS256"])
            member_data["data"] = token_decode
            return jsonify(member_data)

        except jwt.PyJWTError as e:
            print(e)
            member_data["data"] = None
            return jsonify(member_data)

    elif request.method == "PUT":
        data = request.get_data()
        data_read = json.loads(data)

        email = data_read["email"]
        password = data_read["password"]

        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        sign_in = "SELECT password FROM member WHERE email = %s"
        get_name = "SELECT id,name FROM member WHERE email = %s"

        try:
            cursor.execute(sign_in, (email,))
            sign_in_result = cursor.fetchall()

            if sign_in_result == []:
                error["message"] = "輸入錯誤"
                return jsonify(error)

            elif sign_in_result[0][0] != password:
                error["message"] = "密碼錯誤"
                return jsonify(error)

            cursor.execute(get_name, (email,))
            get_name_result = cursor.fetchall()

            token_info = {
                "id": get_name_result[0][0],
                "name": get_name_result[0][1],
                "email": email}
            token = jwt.encode(token_info, "secret", algorithm="HS256")

            resp = make_response(jsonify(sign_in_success))
            resp.set_cookie("token", token, max_age=604800, httponly=True)

            return resp

        except Error as e:
            print(e)
            error["message"] = "伺服器錯誤"
            return jsonify(error)

        finally:
            cnx.close()

    elif request.method == "DELETE":
        resp = make_response(jsonify(sign_in_success))
        resp.set_cookie("token", max_age=-1)

        return resp
