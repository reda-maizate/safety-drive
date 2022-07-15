import json
import pymysql
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import os
import logging


endpoint = os.environ.get("ENDPOINT").split(":")[0]
username = os.environ.get("MASTER_USERNAME")
password = os.environ.get("MASTER_PASSWORD")
db_name = "db_safety_drive"

LOGGER = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
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
        session.execute("SELECT * FROM users")
        result = session.fetchall()
        LOGGER.info(result)
    return templates.TemplateResponse(
        "index.html", {"request": request, "users": json.dumps(result)}
    )


handler = Mangum(app)
