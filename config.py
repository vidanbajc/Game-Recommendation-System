import os
from dotenv import load_dotenv
from logger import logging

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

logging.info("Environment variables loaded successfully")