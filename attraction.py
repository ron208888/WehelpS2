import os
from dotenv import load_dotenv
from flask import *
import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
from flask import Blueprint

attraction = Blueprint("attraction", __name__)
load_dotenv()

dbconfig = {
    "host": "localhost",
    "database": "taipei_day_trip",
    "user": "root",
    "passwd": os.getenv("db_password"),
    "charset": "utf8mb4", "auth_plugin": 'mysql_native_password'}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=3, **dbconfig)


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


def check_total(column, keyword, pages, data):
    cnx = cnxpool.get_connection()
    try:
        cursor = cnx.cursor()
        if column == None and keyword == None:
            cursor.execute("SELECT COUNT(*) FROM attractions;")
            total = cursor.fetchall()[0][0]
            cursor.close()

        elif column == "category":
            cursor.execute(
                "SELECT COUNT(*) FROM attractions WHERE category = %s;", (keyword,))
            total = cursor.fetchall()[0][0]
            cursor.close()

        elif column == "name":
            cursor.execute(
                "SELECT COUNT(*) FROM attractions WHERE name LIKE %s;", (f"%{keyword}%",))
            total = cursor.fetchall()[0][0]
            cursor.close()

        if total/12 > pages + 1:
            data["nextPage"] = pages + 1
            return data
        else:
            data["nextPage"] = None
            return data
    finally:
        cnx.close()


@attraction.route("/api/attractions")
def api_attractions():
    cnx = cnxpool.get_connection()
    try:
        cursor = cnx.cursor()
        page = request.args.get("page")
        keyword = request.args.get("keyword")
        data = {"nextPage": page, "data": {}}
        error_data = {"error": True, "message": ""}
        attraction_list = "SELECT * FROM attractions LIMIT %s,%s"
        cat_search = "SELECT * FROM attractions WHERE category = %s LIMIT %s,%s;"
        name_search = "SELECT * FROM attractions WHERE name LIKE %s LIMIT %s,%s;"

        if keyword == None:
            try:
                pages = int(page)

                cursor.execute(attraction_list, (pages*12, 12))
                attraction_result = cursor.fetchall()
                column = [index[0] for index in cursor.description]
                data_dict = [dict(zip(column, row))
                             for row in attraction_result]

                cursor.close()

                set_img(data_dict)
                correct_data = check_total(
                    None, None,  pages=pages, data=data)
                correct_data["data"] = data_dict

                if correct_data["data"] == []:
                    error_data["message"] = "查無此頁"
                    return jsonify(error_data)

                return jsonify(correct_data)

            except ValueError:
                error_data["message"] = "伺服器錯誤"
                return jsonify(error_data)

        else:

            try:

                pages = int(page)
                cursor = cnx.cursor()
                cursor.execute(cat_search, (keyword, pages*12, pages*12+12))
                cat_result = cursor.fetchall()

                cursor = cnx.cursor()
                cursor.execute(
                    name_search, (f"%{keyword}%", pages*12, pages*12+12))
                name_result = cursor.fetchall()

                if cat_result != [] and name_result == []:
                    column = [index[0] for index in cursor.description]
                    data_dict = [dict(zip(column, row))
                                 for row in cat_result]
                    cursor.close()
                    set_img(data_dict)
                    correct_data = check_total(
                        "category", keyword, pages, data)
                    correct_data["data"] = data_dict
                    return jsonify(correct_data)

                elif cat_result == [] and name_result != []:
                    column = [index[0] for index in cursor.description]
                    data_dict = [dict(zip(column, row))
                                 for row in name_result]
                    cursor.close()
                    set_img(data_dict)
                    correct_data = check_total(
                        "name", keyword, pages, data)
                    correct_data["data"] = data_dict
                    return jsonify(correct_data)
                else:
                    error_data["message"] = "查無資料"
                    return jsonify(error_data)

            except ValueError:
                error_data["message"] = "輸入錯誤"
                return jsonify(error_data)

    finally:
        cnx.close()


@attraction.route("/api/attractions/<attraction_id>/")
def id_search(attraction_id):
    cnx = cnxpool.get_connection()
    try:
        cursor = cnx.cursor()
        search_id = "SELECT * FROM attractions WHERE id = %s"
        data = {"data": {}}
        error = {"error": True, "message": ""}
        img = []

        try:

            cursor.execute(search_id, (attraction_id,))
            id_search_result = cursor.fetchall()

            if id_search_result == []:
                error["message"] = "無此景點編號"
                return jsonify(error)

            column = [index[0] for index in cursor.description]
            data_dict = [dict(zip(column, row)) for row in id_search_result]
            img_split = data_dict[0]["images"].split("https")

            for i in img_split:
                if i != "":
                    img.append(f"https{i}")

            data_dict[0]["images"] = img
            data["data"] = data_dict[0]

            return jsonify(data)

        except Error as e:
            print(e)
            error["message"] = "請輸入數字"
            return jsonify(error)

    finally:
        cnx.close()


@attraction.route("/api/categories")
def categories():
    cnx = cnxpool.get_connection()
    try:
        cursor = cnx.cursor()
        try:
            list_cat = "SELECT DISTINCT category FROM attractions;"
            data = {"data": []}
            error = {"error": True, "message": ""}
            cursor.execute(list_cat)
            categories_list = cursor.fetchall()

            cursor.close()

            for i in categories_list:
                data["data"].append(i[0])

            return jsonify(data)

        except Error as e:
            print(e)
            error["message"] = "伺服器錯誤"
            return jsonify(error)

    finally:
        cnx.close()
