import json
import pymysql
import os
import logging
import boto3

endpoint = os.environ.get("ENDPOINT").split(":")[0]
username = os.environ.get("MASTER_USERNAME")
password = os.environ.get("MASTER_PASSWORD")
db_name = "db_safety_drive"

LOGGER = logging.getLogger(__name__)


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    Lambda function that is triggered by S3 events.
    :param event:
    :param context:
    :return:
    """
    try:
        conn = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            db=db_name,
            connect_timeout=5,
        )
    except pymysql.MySQLError as e:
        LOGGER.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        LOGGER.error(e)

    with conn.cursor() as session:
        session.execute("SELECT * FROM USERS")
        result = session.fetchall()
        LOGGER.info(result)
    return {"statusCode": 200, "users": json.dumps(result)}
