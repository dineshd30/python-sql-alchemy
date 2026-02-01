import sqlalchemy as sa
from sqlalchemy.engine import Connection

engine = sa.create_engine("sqlite:///data/new.db", echo=False)
connection: Connection = engine.connect()

metadata = sa.MetaData()

user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String),
    sa.Column("email", sa.String),
)


def insert_user(conn: Connection, username: str, email: str) -> None:
    """Insert a new user into the user table."""
    query = user_table.insert().values(username=username, email=email)
    conn.execute(query)


def select_users(conn: Connection, username: str = None) -> sa.engine.Result:
    """Select a user by username."""
    query = (
        sa.select(user_table).where(user_table.c.username == username)
        if username
        else sa.select(user_table)
    )
    result = conn.execute(query)
    return result


def main() -> None:
    with engine.begin() as conn:
        metadata.create_all(engine)

        print("Get all users")
        print(select_users(conn).fetchall())

        print("Inserting users")
        insert_user(conn, "alice", "alice@example.com")
        insert_user(conn, "bob", "bob@example.com")

        print("Get user with username 'alice'")
        print(select_users(conn, "alice").fetchall())

        conn.close()


if __name__ == "__main__":
    main()
