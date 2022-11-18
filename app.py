from flask import *
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


connection = mysql.connector.connect(
    host="localhost",
    database="taipei_day_trip",
    user="root",
    passwd="ronally131",
    charset="utf8mb4"
)

cursor = connection.cursor()


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
    if column == None and keyword == None:
        cursor.execute("SELECT COUNT(*) FROM attractions;")
        total = cursor.fetchall()[0][0]
        print(total)
    elif column == "category":
        cursor.execute(
            f"SELECT COUNT(*) FROM attractions WHERE category = '{keyword}';")
        total = cursor.fetchall()[0][0]
        print(total)

    elif column == "name":
        cursor.execute(
            f"SELECT COUNT(*) FROM attractions WHERE name LIKE '%{keyword}%';")
        total = cursor.fetchall()[0][0]
        print(total)

    if total/12 > pages + 1:
        data["nextPage"] = pages + 1
        return data
    else:
        data["nextPage"] = None
        return data


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


@app.route("/api/attractions")
def api_attractions():

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

            cursor.execute(attraction_list, (pages*12, pages*12+12))
            attraction_result = cursor.fetchall()
            column = [index[0] for index in cursor.description]
            data_dict = [dict(zip(column, row))
                         for row in attraction_result]

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

            cursor.execute(cat_search, (keyword, pages*12, pages*12+12))
            cat_result = cursor.fetchall()
            cursor.execute(
                name_search, (f"%{keyword}%", pages*12, pages*12+12))
            name_result = cursor.fetchall()

            if cat_result != [] and name_result == []:
                column = [index[0] for index in cursor.description]
                data_dict = [dict(zip(column, row))
                             for row in cat_result]
                set_img(data_dict)
                correct_data = check_total(
                    "category", keyword, pages, data)
                correct_data["data"] = data_dict
                return jsonify(correct_data)

            elif cat_result == [] and name_result != []:
                column = [index[0] for index in cursor.description]
                data_dict = [dict(zip(column, row))
                             for row in name_result]
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


@app.route("/api/attractions/<attraction_id>/")
def id_search(attraction_id):
    search_id = f"SELECT * FROM attractions WHERE id = {attraction_id}"
    data = {"data": {}}
    error = {"error": True, "message": ""}
    count = 0
    img = []

    try:

        cursor.execute(search_id)
        id_search_result = cursor.fetchall()
        print(id_search_result)
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
        print(data)
        print(attraction_id)
        return jsonify(data)

    except Error as e:
        print(e)
        error["message"] = "請輸入數字"
        return jsonify(error)


app.run(host="0.0.0.0", port=3000)
