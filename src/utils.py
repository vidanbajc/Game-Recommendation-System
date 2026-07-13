import os
import sys
import dill
from src.logger import logging
from src.exception import CustomException


def get_numeric_columns() -> list[str]:
    return ["rating", "ratings_count", "metacritic", "playtime", "release_year"]


def get_categorical_columns() -> list[str]:
    return ["esrb_rating", "release_month"]


def get_list_columns() -> list[str]:
    return ["genres", "platforms", "tags"]


def save_object(file_path: str, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:
            dill.dump(obj, file)

        logging.info(f"Object saved successfully at {file_path}")

    except Exception as e:
        logging.error(f"Error occurred during saving object: {str(e)}")
        raise CustomException(e, sys)

def load_object(file_path: str) -> object:
    try:
        with open(file_path, "rb") as file:
            return dill.load(file)

    except Exception as e:
        logging.error(f"Error occurred during loading object: {str(e)}")
        raise CustomException(e, sys)