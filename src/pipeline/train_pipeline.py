from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


def run_train_pipeline():
    # Data ingestion and cleaning are handled inside the Data Transformation through clean_data()

    transformation = DataTransformation()
    games_arr = transformation.initiate_data_transformation()

    model_trainer = ModelTrainer()
    model_trainer.initiate_model_trainer(games_arr)

if __name__ == "__main__":
    run_train_pipeline()