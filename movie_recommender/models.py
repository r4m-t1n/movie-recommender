from dataclasses import dataclass
import datetime

@dataclass
class User:
    user_id: int

@dataclass
class Account:
    user_id: int
    name: str
    last_name: str | None
    username: str
    hashed_password: str
    creation_date: datetime.date
    last_login: datetime.datetime | None

@dataclass
class Movie:
    movie_id: int
    title: str
    year: int

@dataclass
class Link:
    movie_id: int
    imdb_id: int