import os
import sys
import pandas as pd
from src.utils import load_object
from src.logger import logging
from src.exception import CustomException

class PredictPipeline:

    @staticmethod
    def predict(game_name: str) -> pd.DataFrame:
        try:
            logging.info(f"Finding recommendations for {game_name}")

            model_path = os.path.join("artifacts", "model.pkl")
            games_path = os.path.join("artifacts", "games.pkl")
            games_arr_path = os.path.join("artifacts", "games_arr.pkl")

            model = load_object(model_path)
            games = load_object(games_path)
            games_arr = load_object(games_arr_path)

            game_row = games[games["name"] == game_name]

            if game_row.empty:
                raise ValueError(f"Game {game_name} is not found")

            index = game_row.index[0]
            game_vector = games_arr[index]

            _, indices = model.kneighbors(game_vector, n_neighbors=11)
            recommendations = games.iloc[indices[0][1:]]

            return recommendations

        except Exception as e:
            logging.error(f"Error in game prediction: {str(e)}")
            raise CustomException(e, sys)
        
#df = PredictPipeline.predict("Minecraft")
#df = PredictPipeline.predict("Grand Theft Auto V")
#print(df)