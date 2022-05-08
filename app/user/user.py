from abc import ABC, abstractmethod
from random import random

users = {}


class User(ABC):

    @abstractmethod
    def create_user():
        """create new user"""

    @abstractmethod
    def delete_user(id: str):
        """delete user"""

    @abstractmethod
    def get_user(id: str):
        """get a user"""


class BusinessUser(User):

    def create_user(data: dict):
        uuid = random(0, 1)*10 + random(0, 1) * 0.002
        users[uuid] = data
        return {u'uuid': uuid, **data}

    def delete_user(id: str):
        users.pop(id)
        return "user has been removed from storage"

    def get_user(id: str):
        return {u'uuid': id, **users[id]}
