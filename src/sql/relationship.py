import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = sa.create_engine("sqlite:///data/users.db", echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    # One-to-one relationship with Address
    address: Mapped["Address"] = relationship(
        "Address", back_populates="user", uselist=False
    )

    # One-to-many relationship with Post
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    street: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()

    # Bidirectional relationship with User
    user: Mapped[User] = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        return (
            f"Address(id={self.id}, street={self.street}, city={self.city}, "
            f"state={self.state}, zip_code={self.zip_code})"
        )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()

    # Bidirectional relationship with User
    user: Mapped[User] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, content={self.content})"


def main() -> None:
    Base.metadata.create_all(engine)

    with session() as sess:
        print("All users:")
        users = sess.query(User).all()
        print(users)

        print("Inserting a new user with address and posts:")
        user = User(
            username="alice",
            email="alice@example.com",
            address=Address(
                street="123 Main St", city="Wonderland", state="WL", zip_code="12345"
            ),
            posts=[
                Post(title="First Post", content="This is my first post!"),
                Post(title="Second Post", content="This is my second post!"),
            ],
        )
        sess.add(user)
        sess.commit()

        print("All users after insertion:")
        users = sess.query(User).all()
        print(users)

        print("User's address and posts:")
        print(user.address)
        print(user.posts)
        sess.close()


if __name__ == "__main__":
    main()
