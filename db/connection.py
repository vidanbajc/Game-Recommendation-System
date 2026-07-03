import os
import sys
import json
import mysql.connector
from config import MYSQL_USER, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_DATABASE
from src.exception import CustomException

JSON_PATH = os.path.join("data", "raw", "games.json")

try:
    with open(JSON_PATH, "r") as file:
        data = json.load(file)

except Exception as e:
    raise CustomException(e, sys)


try:
    con = mysql.connector.connect(
        user=MYSQL_USER,
        host=MYSQL_HOST,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    print("Connected...")

except Exception as e:
    raise CustomException(e, sys)