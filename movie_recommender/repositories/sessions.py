import psycopg
from models import Session

class SessionRepository:
    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def create_session(self, session: Session):
        self.connection.execute(
            "INSERT INTO sessions (user_id, token_hash, expires_at) VALUES "
            "(%s, %s, %s)",
            (session.user_id, session.token_hash, session.expires_at))

    def get_session(self, token_hash: str) -> Session | None:
        result = self.connection.execute(
            "SELECT session_id, user_id, token_hash, created_at, expires_at "
            "FROM sessions WHERE token_hash = %s and expires_at > CURRENT_TIMESTAMP", (token_hash,)
        ).fetchone()

        if result is None:
            return None
        else:
            return Session(*result)

    def delete_session(self, token_hash: str):
        result = self.connection.execute(
            "DELETE FROM sessions WHERE token_hash = %s RETURNING 1",
            (token_hash,)
        ).fetchone()

        if result:
            return True
        return False