from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"
