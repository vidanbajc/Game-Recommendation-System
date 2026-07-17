import os
import sys
import pandas as pd
from db.connection import get_engine
from src.utils import load_object
from src.logger import logging
from src.exception import CustomException

model_path = os.path.join("artifacts", "model.pkl")
games_arr_path = os.path.join("artifacts", "games_arr.pkl")
games_meta_path = os.path.join("artifacts", "games_meta.pkl")

MODEL = load_object(model_path)
GAMES_ARR = load_object(games_arr_path)
GAMES_META = load_object(games_meta_path)
engine = get_engine()

class PredictPipeline:

    @staticmethod
    def recommend(game_name: str) -> pd.DataFrame:
        try:
            
            logging.info(f"Finding recommendations for {game_name}")

            game_row = GAMES_META[GAMES_META["name"].str.lower() == game_name.strip().lower()]

            if game_row.empty:
                raise ValueError(f"Game {game_name} is not found")
            
            index = game_row.index[0]
            game_vector = GAMES_ARR[index]

            _, indices = MODEL.kneighbors(game_vector, n_neighbors=11)
            ids = GAMES_META.iloc[indices[0][1:]]["id"].tolist()

            placeholders = ", ".join(["%s"] * len(ids))
            query = f"select id, name, image_url from games where id in ({placeholders})"
            recommendations = pd.read_sql(query, engine, params=tuple(ids))

            return recommendations

        except ValueError:
            raise

        except Exception as e:
            logging.error(f"Error in game recommendation: {str(e)}")
            raise CustomException(e, sys)
        
#df = PredictPipeline.recommend("Minecraft")
#df = PredictPipeline.recommend("Grand Theft Auto V")
#print("\n", df)