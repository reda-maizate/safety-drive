import json
import logging
import os

import pymysql
from fastapi import FastAPI, Depends, status, Request

# from fastapi.responses import RedirectResponse, HTMLResponse
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_login import LoginManager
# from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

LOGGER = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

endpoint = os.environ.get("ENDPOINT").split(":")[0]
username = os.environ.get("MASTER_USERNAME")
password = os.environ.get("MASTER_PASSWORD")
db_name = "db_safety_drive"

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

# SECRET = os.environ.get("SECRET_LOGIN")

pth = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(pth, "templates"))

# manager = LoginManager(
#     SECRET,
#     token_url="/auth/login",
#     use_cookie=True,
#     cookie_name="safety_drive_cookie",
#     use_header=False,
# )


# @manager.user_loader()
# def load_user(user_name: str):
#     with conn.cursor() as session:
#         session.execute(f"# SELECT * FROM USERS WHERE pseudo = '{user_name}'")
#         user = session.fetchone()
#     return user


# @app.post("/auth/login")
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     input_username = data.username
#     input_password = data.password
#     user = load_user(input_username)
#
# if not user or input_password != user[2]:
#     raise InvalidCredentialsException
#
# access_token = manager.create_access_token(data={"sub": input_username})
# resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)
# manager.set_cookie(resp, access_token)
# return resp


@app.get("/{user_name}")
def get_private_endpoint(request: Request, user_name: str):
    with conn.cursor() as session:
        session.execute(f"SELECT * FROM PREDICTIONS WHERE user = {user_name}")
        result = session.fetchall()

    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.DataFrame(
        result, columns=["prediction_id", "prediction", "datetime", "user_id"]
    )
    # Create a simple plot with the column prediction and datetime of the dataframe df
    df.plot(x="datetime", y="prediction", figsize=(20, 10))
    # Save the plot to a file
    plt.savefig("static/plot.png")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "predictions": json.dumps(result, default=str),
            "graph": "plot.png",
        },
    )


# @app.get("/", response_class=HTMLResponse)
# def login_with_creds(request: Request):
#     with open(os.path.join(pth, "templates/login.html")) as f:
#         return HTMLResponse(content=f.read())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

# handler = Mangum(app)
