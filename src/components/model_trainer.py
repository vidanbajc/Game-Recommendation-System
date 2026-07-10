import os
import sys
from sklearn.neighbors import NearestNeighbors
from src.logger import logging
from src.utils import save_object
from src.exception import CustomException


class ModelTrainerConfig:
    def __init__(self):
        self.similarity_matrix_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, games_arr):
        try:
            logging.info("Training NearestNeighbors model")

            model = NearestNeighbors(n_neighbors=10, metric="cosine", algorithm="brute")
            model.fit(games_arr)

            logging.info("NearestNeighbors model trained successfully")

            save_object(
                file_path=self.model_trainer_config.similarity_matrix_file_path,
                obj=model
            )

        except Exception as e:
            logging.error(f"Error in model trainer: {str(e)}")
            raise CustomException(e,sys)
        
    