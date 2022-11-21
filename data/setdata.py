import mysql.connector
from mysql.connector import Error
import json
from copy import deepcopy

with open("taipei-attractions.json", encoding="utf-8") as f:
    data = json.load(f)
    result = data["result"]["results"]

    print(type(result))
try:
    connection = mysql.connector.connect(
        host="localhost",
        database="taipei_day_trip",
        user="root",
        passwd="12345678",
        charset="utf8mb3"
    )
    cursor = connection.cursor()
    count = 0
    img = {}
    fuck = []
    l = 0
    for i in result:
        count += 1

        clear = i["file"].split("https")
        img[count] = []
        for j in clear:
            if ".jpg" not in ("" + j + "") and ".png" not in ("" + j + "") and ".JPG" not in ("" + j + "") and ".PNG" not in ("" + j + ""):
                fuck.append([count, j])
            else:
                img[count].append(f"https{j}")

    add_data = "INSERT INTO attractions(id,name,category,description,address,transport,mrt,lat,lng,images) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    count = 0
    for x in result:
        id = x["_id"]
        name = x["name"]
        category = x["CAT"]
        description = x["description"]
        address = x["address"]
        transport = x["direction"]
        mrt = x["MRT"]
        lat = x["latitude"]
        lng = x["longitude"]

        count += 1
        x["file"] = "".join(img[count])
        images = x["file"]

        # print(name,category,description,address,transport,mrt,lat,lng,images)

        cursor.execute(add_data, (id, name, category,
                                  description, address, transport, mrt, lat, lng, images))
        connection.commit()
        print("寫入成功")


except Error as e:
    print(e)

# try:
#     connection = mysql.connector.connect(
#         host="localhost",
#         database="taipei_day_trip",
#         user="root",
#         passwd="12345678",
#         charset="utf8mb3"
#     )

#     if connection.is_connected():
#         cursor = connection.cursor()
#         add_data = "INSERT INTO attractions(id,name,category,description,address,transport,mrt,lat,lng) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"

#         for i in result:
#             id = i["_id"]
#             name = i["name"]
#             category = i["CAT"]
#             description = i["description"]
#             address = i["address"]
#             transport = i["direction"]
#             mrt = i["MRT"]
#             lat = i["latitude"]
#             lng = i["longitude"]

#             # print(name,category,description,address,transport,mrt,lat,lng,images)

#             cursor.execute(add_data, (id, name, category,
#                            description, address, transport, mrt, lat, lng))
#             connection.commit()
#             print("寫入成功")


# except Error as e:
#     print(e)
