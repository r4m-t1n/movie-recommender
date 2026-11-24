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
class Session:
    session_id: int
    user_id: int
    token_hash: str
    created_at: datetime.datetime | None
    expires_at: datetime.datetime

@dataclass
class Movie:
    movie_id: int
    title: str
    year: int

@dataclass
class Link:
    movie_id: int
    imdb_id: int