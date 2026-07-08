import sys
from db.connection import load_data, get_connection
from src.logger import logging
from src.exception import CustomException

con = get_connection()
cur = con.cursor()

try:
    cur.execute("select id from genres")
    genre_set = set(x[0] for x in cur.fetchall())

    cur.execute("select id from platforms")
    platform_set = set(x[0] for x in cur.fetchall())

    cur.execute("select id from tags")
    tag_set = set(x[0] for x in cur.fetchall())

except Exception as e:
    raise CustomException(e, sys)

logging.info("Updating database")

data = load_data()

for game in data:
    try:
        values = (game["id"], game["name"], game["released"], game["rating"], game["ratings_count"], 
                   game["metacritic"], game["playtime"], game["esrb_rating"]["name"] if game.get("esrb_rating") else None)
        query = "insert ignore into games(id, name, released, rating, ratings_count, metacritic, playtime, esrb_rating) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, values)

        for genre in game["genres"]:

            id = genre["id"]
            name = genre["name"]

            if id not in genre_set:
                genre_set.add(id)

                values = (id, name)
                query = "insert ignore into genres(id, name) values (%s, %s)"
                cur.execute(query, values)

            values = (game["id"], id)
            query = "insert ignore into game_genres(game_id, genre_id) values (%s, %s)"
            cur.execute(query, values)

        for platform in game["platforms"]:

            id = platform["platform"]["id"]
            name = platform["platform"]["name"]

            if id not in platform_set:
                platform_set.add(id)

                values = (id, name)
                query = "insert ignore into platforms(id, name) values (%s, %s)"
                cur.execute(query, values)

            values = (game["id"], id)
            query = "insert ignore into game_platforms(game_id, platform_id) values (%s, %s)"
            cur.execute(query, values)

        for tag in game["tags"]:

            id = tag["id"]
            name = tag["name"]

            if id not in tag_set:
                tag_set.add(id)

                values = (id, name)
                query = "insert ignore into tags(id, name) values (%s, %s)"
                cur.execute(query, values)

            values = (game["id"], id)
            query = "insert ignore into game_tags(game_id, tag_id) values (%s, %s)"
            cur.execute(query, values)

    except Exception as e:
        logging.error(f"Error processing game_id = {game['id']}")
        raise CustomException(e, sys) 

con.commit()
logging.info("Database successfully updated")

cur.close()
con.close()