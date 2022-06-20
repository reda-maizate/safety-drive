import json
import pymysql
import os


def lambda_handler(event, context):
    endpoint = os.environ.get("ENDPOINT").split(":")[0]
    username = os.environ.get("MASTER_USERNAME")
    password = os.environ.get("MASTER_PASSWORD")

    # print("Globals", endpoint)
    # print("Globals", username)
    # print("Globals", password)

    db = pymysql.connect(
        # ToDo
        host=endpoint,  # Point de terminaison
        user=username,
        password=password,
        port=3306,
    )
    cursor = db.cursor()
    sql = """use db_safety_drive"""
    cursor.execute(sql)
    cursor.execute("SELECT * FROM USERS")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    return {"statusCode": 200, "body": "OK"}
