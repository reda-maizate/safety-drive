import json
import pymysql
import os


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    Lambda function that is triggered by S3 events.
    :param event:
    :param context:
    :return:
    """
    endpoint = os.environ.get("ENDPOINT").split(":")[0]
    username = os.environ.get("MASTER_USERNAME")
    password = os.environ.get("MASTER_PASSWORD")

    # print("Globals", endpoint)
    # print("Globals", username)
    # print("Globals", password)

    database = pymysql.connect(
        # ToDo
        host=endpoint,  # Point de terminaison
        user=username,
        password=password,
        port=3306,
    )
    cursor = database.cursor()
    sql = """use db_safety_drive"""
    cursor.execute(sql)
    cursor.execute("SELECT * FROM USERS")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    return {"statusCode": 200, "body": "OK"}
