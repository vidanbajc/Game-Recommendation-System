import sys
import pandas as pd
from sqlalchemy import create_engine
from config import MYSQL_USER, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_DATABASE
from urllib.parse import quote_plus
from logger import logging
from src.exception import CustomException

try:
    password = quote_plus(MYSQL_PASSWORD)
    engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{password}@{MYSQL_HOST}/{MYSQL_DATABASE}")

except Exception as e:
    raise CustomException(e, sys)


class DataIngestion:
    def __init__(self, engine):
        self.engine = engine

    def load_data(self) -> dict[str, pd.DataFrame]:
        try:
            logging.info("Starting data ingestion")

            games = pd.read_sql("select * from games", self.engine)
            genres = pd.read_sql("select * from genres", self.engine)
            game_genres = pd.read_sql("select * from game_genres", self.engine)
            platforms = pd.read_sql("select * from platforms", self.engine)
            game_platforms = pd.read_sql("select * from game_platforms", self.engine)
            tags = pd.read_sql("select * from tags", self.engine)
            game_tags = pd.read_sql("select * from game_tags", self.engine)

            logging.info("Data ingestion completed successfully")

            return {
                "games": games,
                "genres": genres,
                "game_genres": game_genres,
                "platforms": platforms,
                "game_platforms": game_platforms,
                "tags": tags,
                "game_tags": game_tags,
            }

        except Exception as e:
            logging.error(f"Data ingestion failed while reading from MySQL database: {MYSQL_DATABASE}")
            raise CustomException(e, sys)
        
# ingestion = DataIngestion(engine)

# data = ingestion.load_data()
# games = data["games"]

# print(games.head())