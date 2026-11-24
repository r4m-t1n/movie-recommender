from datetime import datetime
import psycopg
from models import Account

class AccountRepository:
    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def add_account(self, account: Account):
        self.connection.execute("INSERT INTO accounts "
            "(user_id, name, last_name, username, hashed_password)"
            "VALUES (%s, %s, %s, %s, %s)",
            (account.user_id, account.name, account.last_name,
            account.username, account.hashed_password))

    def get_by_username(self, username: str):
        result =  self.connection.execute(
            "SELECT user_id, name, last_name, username, hashed_password, "
            "creation_date, last_login FROM accounts WHERE username = %s", 
            (username,)).fetchone()
        if result is None:
            return None
        else:
            return Account(*result)

    def delete_account(self, username: str):
        self.connection.execute("DELETE FROM accounts WHERE username = %s", (username,))

    def change_password(self, username: str, new_hashed_password: str):
        self.connection.execute("UPDATE accounts SET hashed_password = %s "
            "WHERE username = %s", (new_hashed_password, username))

    def update_last_login(self, username: str, timestamp: datetime = None):
        if timestamp is None:
            self.connection.execute("UPDATE accounts SET last_login = CURRENT_TIMESTAMP "
                "WHERE username = %s", (username,))
        else:
            self.connection.execute("UPDATE accounts SET last_login = %s "
                "WHERE username = %s", (timestamp, username))