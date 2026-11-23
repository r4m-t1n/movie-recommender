import os
import csv
from pathlib import Path
from psycopg import Connection
from movie_recommender import db

def extract_users(path: str, users_set: set, conn: Connection):

    users_serial = 0 if not len(users_set) else max(users_set)

    with open(path, 'r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for new_line in reader:
            if int(new_line["userId"]) not in users_set:
                conn.execute("INSERT INTO users VALUES (%s)", (new_line["userId"], ))
                users_set.add(int(new_line["userId"]))
                users_serial = max(users_serial, int(new_line["userId"]))

        conn.execute("SELECT setval(pg_get_serial_sequence('users', 'user_id'), %s)", (users_serial,))

def extract_movies(movies_path, conn):
    movies_serial = 0

    with open(movies_path, 'r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for new_line in reader:

            movies_serial = max(movies_serial, int(new_line["movieId"]))

            year_in_p = None
            new_line["title"] = new_line["title"].strip()
            if (len(new_line["title"])>=6):
                year_in_p = new_line["title"][-6:]

            year = None
            if (year_in_p is not None and year_in_p[0] == '(' and year_in_p[5] == ')' and year_in_p[1:5].isdigit()):
                year = year_in_p[1:5]    
                new_line["title"] = new_line["title"][:-6].strip()

            conn.execute(
                "INSERT INTO movies (movie_id, title, year) VALUES (%s, %s, %s)",
                (new_line["movieId"], new_line["title"], year))

            for genre_type in new_line["genres"].split('|'):
                if genre_type == "(no genres listed)":
                    break
                conn.execute(
                    "INSERT INTO genres (movie_id, genre_type) VALUES (%s, %s)",
                    (new_line["movieId"], genre_type))

        conn.execute("SELECT setval(pg_get_serial_sequence('movies', 'movie_id'), %s)", (movies_serial,))



def extract_tags(tags_path, conn):
    with open(tags_path, 'r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for new_line in reader:
            conn.execute(
                "INSERT INTO tags (user_id, movie_id, tag, tagged_at) VALUES (%s, %s, %s, to_timestamp(%s))",
                (new_line["userId"], new_line["movieId"], new_line["tag"], new_line["timestamp"]))


def extract_ratings(ratings_path, conn):
    with open(ratings_path, 'r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for new_line in reader:
            conn.execute(
                "INSERT INTO ratings (user_id, movie_id, rating, rated_at) VALUES (%s, %s, %s, to_timestamp(%s))",
                (new_line["userId"], new_line["movieId"], new_line["rating"], new_line["timestamp"]))


def extract_links(links_path, conn):
    with open(links_path, 'r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for new_line in reader:
            conn.execute("INSERT INTO links (movie_id, imdb_id) VALUES (%s, %s)",
                        (new_line["movieId"], new_line["imdbId"]))


if __name__ == "__main__":

    BASE_PATH = Path(__file__).parent.parent / Path("data")
    FOLDER_NAME = Path("ml-latest-small")
    PATH = BASE_PATH / FOLDER_NAME

    LINKS_PATH = PATH / Path("links.csv")
    MOVIES_PATH = PATH / Path("movies.csv")
    RATINGS_PATH = PATH / Path("ratings.csv")
    TAGS_PATH = PATH / Path("tags.csv")

    if not os.path.exists(PATH):
        import zipfile
        for file in os.listdir(BASE_PATH):
            if not file.endswith(".zip"):
                continue

            with zipfile.ZipFile(BASE_PATH / Path(file), 'r') as zip_ref:
                zip_ref.extractall(BASE_PATH)

    if not os.path.exists(MOVIES_PATH):
        raise RuntimeError("movies.csv not found")

    if not os.path.exists(LINKS_PATH):
        raise RuntimeError("links.csv not found")

    if not os.path.exists(RATINGS_PATH):
        raise RuntimeError("ratings.csv not found")

    if not os.path.exists(TAGS_PATH):
        raise RuntimeError("tags.csv not found")

    users_set = set()
    with db.connect() as conn:
        extract_users(TAGS_PATH, users_set, conn)
        extract_users(RATINGS_PATH, users_set, conn)
        extract_movies(MOVIES_PATH, conn)
        extract_tags(TAGS_PATH, conn)
        extract_ratings(RATINGS_PATH, conn)
        extract_links(LINKS_PATH, conn)