import sys
import pymysql


def run():
    if len(sys.argv) == 4:
        endpoint = sys.argv[1].split(":")[0]
        username = sys.argv[2]
        password = sys.argv[3]

        db = pymysql.connect(
            host=endpoint,  # Point de terminaison
            user=username,
            password=password,
            port=3306,
        )
        cursor = db.cursor()

        cursor.connection.commit()
        sql = """use db_safety_drive"""
        cursor.execute(sql)

        sql = """CREATE TABLE USERS (id_user varchar(512)  primary key, email varchar(128) not null, password varchar(512) not null, pseudo varchar(128) not null)"""
        cursor.execute(sql)
        sql = """CREATE TABLE PREDICTIONS (id_prediction integer primary key auto_increment, value integer not null, datetime datetime not null, user integer references USERS(id_user))"""
        cursor.execute(sql)
        users_row = """INSERT INTO USERS (id_user, email, password, pseudo) VALUES ("1", "test@test.com", "test", "test")"""
        cursor.execute(users_row)
        predictions_row = """INSERT INTO PREDICTIONS (value, datetime, user) VALUES (1, "2020-01-01 00:00:00", "1"),
                                                                                    (2, "2020-01-01 01:00:00", "1"),
                                                                                    (2, "2020-01-01 02:00:00", "1"),
                                                                                    (2, "2020-01-01 03:00:00", "1"),
                                                                                    (4, "2020-01-01 04:00:00", "1"),
                                                                                    (4, "2020-01-01 05:00:00", "1"),
                                                                                    (8, "2020-01-01 06:00:00", "1"),
                                                                                    (9, "2020-01-01 07:00:00", "1"),
                                                                                    (9, "2020-01-01 08:00:00", "1"),
                                                                                    (9, "2020-01-01 09:00:00", "1"),
                                                                                    (9, "2020-01-01 10:00:00", "1"),
                                                                                    (9, "2020-01-01 11:00:00", "1"),
                                                                                    (9, "2020-01-01 12:00:00", "1"),
                                                                                    (9, "2020-01-01 13:00:00", "1"),
                                                                                    (9, "2020-01-01 14:00:00", "1"),
                                                                                    (9, "2020-01-01 15:00:00", "1"),
                                                                                    (9, "2020-01-01 16:00:00", "1"),
                                                                                    (5, "2020-01-01 17:00:00", "1"),
                                                                                    (9, "2020-01-01 18:00:00", "1"),
                                                                                    (9, "2020-01-01 19:00:00", "1"),
                                                                                    (9, "2020-01-01 20:00:00", "1"),
                                                                                    (9, "2020-01-01 21:00:00", "1"),
                                                                                    (4, "2020-01-01 22:00:00", "1"),
                                                                                    (4, "2020-01-01 23:00:00", "1"),
                                                                                    (4, "2020-01-01 24:00:00", "1")"""
        cursor.execute(predictions_row)
    else:
        print(
            f'Argument(s) missing, try : "python script_create_db.py (endpoint) (user_db) (password_db)"'
        )


if __name__ == "__main__":
    run()
