import sys
import pymysql


def run():
    if len(sys.argv) == 4:
        endpoint = sys.argv[1].split(':')[0]
        username = sys.argv[2]
        password = sys.argv[3]

        db = pymysql.connect(
            # ToDo
            host=endpoint,  # Point de terminaison
            user=username,
            password=password,
            port=3306
        )
        cursor = db.cursor()

        sql = '''create database db_safety_drive'''
        cursor.execute(sql)

        cursor.connection.commit()
        sql = '''use db_safety_drive'''
        cursor.execute(sql)

        sql = '''CREATE TABLE USERS (id_user integer primary key, email varchar(128) not null, password varchar(512) not null, pseudo varchar(128) not null)'''
        cursor.execute(sql)
        sql = '''CREATE TABLE PREDICTIONS (id_prediction integer primary key, value integer not null, datetime datetime not null, user integer references USERS(id_user))'''
        cursor.execute(sql)
    else:
        print(f"Argument(s) missing, try : \"python script_create_db.py (endpoint) (user_db) (password_db)\"")


if __name__ == '__main__':
    run()