import os
import sys
import json
import mysql.connector
from sqlalchemy import create_engine
from config import MYSQL_USER, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_DATABASE
from urllib.parse import quote_plus
from src.logger import logging
from src.exception import CustomException

JSON_PATH = os.path.join("data", "raw", "games.json")

def load_data():
    try:
        logging.info(f"Reading JSON file {JSON_PATH}")
        with open(JSON_PATH, "r") as file:
            data = json.load(file)

        return data

    except Exception as e:
        logging.error(f"Failed to read JSON file: {JSON_PATH}")
        raise CustomException(e, sys)

def get_connection() -> mysql.connector.MySQLConnection:
    try:
        logging.info(f"Connecting to MySQL database: {MYSQL_DATABASE}")
        con = mysql.connector.connect(
            user=MYSQL_USER,
            host=MYSQL_HOST,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        return con

    except Exception as e:
        logging.error(f"Failed to connect to MySQL database: {MYSQL_DATABASE}")
        raise CustomException(e, sys)

def get_engine():
    try:
        password = quote_plus(MYSQL_PASSWORD)
        engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{password}@{MYSQL_HOST}/{MYSQL_DATABASE}")
        return engine

    except Exception as e:
        raise CustomException(e, sys)