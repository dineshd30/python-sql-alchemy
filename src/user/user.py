from typing import List

from pydantic import BaseModel

from model import Address, Post, User
from sql import Address as SQLAddress
from sql import Post as SQLPost
from sql import User as SQLUser
from sql import get_session


class User(BaseModel):
    def __init__(self):
        self.session = get_session()

    def add(self, user: User, address: Address, posts: List[Post]):
        with self.session as session:
            sql_user = SQLUser(
                username=user.username,
                email=user.email,
                address=SQLAddress(
                    street=address.street,
                    city=address.city,
                    state=address.state,
                    zip_code=address.zip_code,
                ),
                posts=[
                    SQLPost(title=post.title, content=post.content) for post in posts
                ],
            )
            session.add(sql_user)
            session.commit()

    def get(self):
        pass

    def get_all(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
