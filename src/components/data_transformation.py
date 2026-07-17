import os
import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.components.data_cleaning import clean_data
from src.utils import get_numeric_columns, get_categorical_columns, get_list_columns, save_object
from src.logger import logging
from src.exception import CustomException

class DataTransformationConfig:
    def __init__(self):
        self.preprocessor_file_path = os.path.join("artifacts", "preprocessor.pkl")
        #self.games_id_name_file_path = os.path.join("artifacts", "games.pkl")
        self.games_meta_file_path = os.path.join("artifacts", "games_meta.pkl")
        self.games_arr_file_path = os.path.join("artifacts", "games_arr.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def load_and_merge_data(self, clean_data: dict[str, pd.DataFrame]) -> pd.DataFrame:

        logging.info("Loading cleaned data")

        # Loading cleaned data
        games = clean_data["games"]
        genres = clean_data["genres"]
        game_genres = clean_data["game_genres"]
        platforms = clean_data["platforms"]
        game_platforms = clean_data["game_platforms"]
        tags = clean_data["tags"]
        game_tags = clean_data["game_tags"]

        # Merge game types with their names
        game_genres = game_genres.merge(genres, left_on="genre_id", right_on="id", how="left")
        game_platforms = game_platforms.merge(platforms, left_on="platform_id", right_on="id", how="left")
        game_tags = game_tags.merge(tags, left_on="tag_id", right_on="id", how="left")

        # Group by game_id and combine all names into lists
        genres = game_genres.groupby("game_id")["name"].apply(list).reset_index()
        platforms = game_platforms.groupby("game_id")["name"].apply(list).reset_index()
        tags = game_tags.groupby("game_id")["name"].apply(list).reset_index()

        # Rename columns for better readability
        genres.rename(columns={"name": "genres"}, inplace=True)
        platforms.rename(columns={"name": "platforms"}, inplace=True)
        tags.rename(columns={"name": "tags"}, inplace=True)

        # Merging all data with games and removing duplicated game_id
        games = games.merge(genres, left_on="id", right_on="game_id", how="left")
        games = games.drop(columns=["game_id"])

        games = games.merge(platforms, left_on="id", right_on="game_id", how="left")
        games = games.drop(columns=["game_id"])

        games = games.merge(tags, left_on="id", right_on="game_id", how="left")
        games = games.drop(columns=["game_id"])

        # Convert list values into strings for easier processing with TfidfVectorizer
        games["genres"] = games["genres"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
        games["platforms"] = games["platforms"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
        games["tags"] = games["tags"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

        #print("NaN Values: ", games.isna().sum())

        logging.info("Loading and merging data successfully")
        return games

    def get_preprocessor(self) -> ColumnTransformer:
        try:
            logging.info("Creating preprocessing pipeline")

            num_columns = get_numeric_columns()
            cat_columns = get_categorical_columns()
            #list_columns = get_list_columns()

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("one_hot_encoder", OneHotEncoder())
                ]
            )

            list_pipeline = Pipeline(
                steps=[
                    ("tf-idf", TfidfVectorizer())
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, num_columns),
                    ("cat_pipeline", cat_pipeline, cat_columns),
                    ("genres", list_pipeline, "genres"),
                    ("platforms", list_pipeline, "platforms"),
                    ("tags", list_pipeline, "tags")
                ],

                transformer_weights={
                    "num_pipeline": 0.1,
                    "cat_pipeline": 0.1,
                    "genres": 1.5,
                    "tags": 3,
                    "platforms": 0.5
                }
            )

            logging.info("Preprocessing pipeline created successfully")

            return preprocessor

        except Exception as e:
            logging.error(f"Error while creating preprocessing pipeline: {str(e)}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Building preprocessing pipeline")

            games = self.load_and_merge_data(clean_data())
            preprocessor = self.get_preprocessor()

            games_meta = games[["id", "name"]].reset_index(drop=True)
            games_arr = preprocessor.fit_transform(games)

            logging.info("Data transformation completed successfully")

            save_object(
                file_path=self.data_transformation_config.preprocessor_file_path,
                obj=preprocessor
            )

            save_object(
                file_path=self.data_transformation_config.games_arr_file_path,
                obj=games_arr
            )

            save_object(
                file_path=self.data_transformation_config.games_meta_file_path,
                obj=games_meta
            )

            return games_arr

        except Exception as e:
            logging.error(f"Error occurred during data transformation: {str(e)}")
            raise CustomException(e, sys)
