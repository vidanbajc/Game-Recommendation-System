import os
import sys
import requests
import json
import time
from config import RAWG_API_KEY
from src.exception import CustomException

URL = f"https://api.rawg.io/api/games"
JSON_PATH = os.path.join("data", "raw", "games.json")

games = []
page = 1
page_size = 40

while len(games) < 5000:
    params = {
        "key": RAWG_API_KEY,
        "page_size": page_size,
        "page": page
    }

    try:
        response = requests.get(URL, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        games.extend(results)

        page += 1
        time.sleep(1)

        print("Number of games: ", len(games))

    except Exception as e:
        raise CustomException(e, sys)

try:
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(games, file, indent=4)

except Exception as e:
    raise CustomException(e, sys)

print("Done...")
