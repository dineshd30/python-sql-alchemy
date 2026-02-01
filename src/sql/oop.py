import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker

engine = sa.create_engine("sqlite:///data/new.db", echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


def main() -> None:
    Base.metadata.create_all(engine)

    with session() as sess:
        print("All users:")
        users = sess.query(User).all()
        print(users)

        print("Inserting a new user:")
        user = User(username="alice", email="alice@example.com")
        sess.add(user)
        sess.commit()

        print("All users after insertion:")
        users = sess.query(User).all()
        print(users)


if __name__ == "__main__":
    main()
