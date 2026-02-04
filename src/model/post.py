from pydantic import BaseModel


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, content={self.content})"
