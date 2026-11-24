import secrets
import hashlib
import datetime

import psycopg
import argon2

from movie_recommender import db
from movie_recommender.models import Account, Session
from movie_recommender.repositories.accounts import AccountRepository
from movie_recommender.repositories.sessions import SessionRepository

password_hasher = argon2.PasswordHasher()

TOKEN_AVAILABILITY = 3600 * 4

def generate_hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def generate_token(repo: SessionRepository) -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = generate_hash_token(token)
    while repo.get_session(token_hash) is not None:
        token = secrets.token_urlsafe(32)
        token_hash = generate_hash_token(token)

    return token, token_hash

def register(username: str, password: str, name: str, last_name: str | None = None) -> bool:
    try:
        with db.connect() as conn:
            acc_rep = AccountRepository(conn)

            found_account = acc_rep.get_by_username(username)

            if (found_account is not None):
                return False

            hashed_password = password_hasher.hash(password)

            user_id = acc_rep.add_user()

            created_account = Account(
                user_id,
                name,
                last_name,
                username,
                hashed_password,
                None,
                None
            )
            acc_rep.add_account(created_account)

            return True
    except psycopg.errors.UniqueViolation:
        return False

def login(username: str, password: str) -> str | None:
    with db.connect() as conn:
        acc_rep = AccountRepository(conn)

        account = acc_rep.get_by_username(username)

        if account is None:
            return None

        try:
            password_hasher.verify(account.hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return None

        acc_rep.update_last_login(username, None)

        session_rep = SessionRepository(conn)
        token, token_hash = generate_token(session_rep)

        new_session = Session(
            None,
            account.user_id,
            token_hash,
            None,
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=TOKEN_AVAILABILITY)
        )
        session_rep.create_session(new_session)

        return token

def authenticate(token: str) -> int | None:
    with db.connect() as conn:
        session_rep = SessionRepository(conn)

        token_hash = generate_hash_token(token)

        session = session_rep.get_session(token_hash)

        if session is None:
            return None

        return session.user_id

def log_out(token: str):
    with db.connect() as conn:
        session_rep = SessionRepository(conn)
        token_hash = generate_hash_token(token)
        return session_rep.delete_session(token_hash)