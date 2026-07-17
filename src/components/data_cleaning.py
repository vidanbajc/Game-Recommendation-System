import pandas as pd
from src.components.data_ingestion import DataIngestion
from db.connection import get_engine

def clear_games(games: pd.DataFrame) -> pd.DataFrame:

    games["released"] = pd.to_datetime(games["released"])
    games["release_year"] = games["released"].dt.year
    #games["release_month"] = games["released"].dt.month
    #games["release_month"] = games["release_month"].astype("object")
    games.drop(columns=["released", "image_url"], inplace=True)

    games["esrb_rating"] = games["esrb_rating"].fillna("Unknown")
    games["has_metacritic"] = games["metacritic"].notna().astype(int)
    games["metacritic"] = games["metacritic"].fillna(games["metacritic"].median())

    return games

def clean_data() -> dict[str, pd.DataFrame]:
    engine = get_engine()
    ingestion = DataIngestion(engine)
    data = ingestion.load_data()

    data["games"] = clear_games(data["games"])

    return data