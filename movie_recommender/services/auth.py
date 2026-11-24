import psycopg
import argon2

from movie_recommender import db
from movie_recommender.models import Account
from movie_recommender.repositories.accounts import AccountRepository

password_hasher = argon2.PasswordHasher()

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

def login(username: str, password: str) -> bool:
    with db.connect() as conn:
        acc_rep = AccountRepository(conn)

        account = acc_rep.get_by_username(username)

        if account is None:
            return False

        try:
            password_hasher.verify(account.hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

        acc_rep.update_last_login(username, None)

        return True
