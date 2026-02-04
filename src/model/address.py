from pydantic import BaseModel


class Address(BaseModel):
    id: int
    user_id: int
    street: str
    city: str
    state: str
    zip_code: str

    def __repr__(self) -> str:
        return (
            f"Address(id={self.id}, street={self.street}, city={self.city}, "
            f"state={self.state}, zip_code={self.zip_code})"
        )
