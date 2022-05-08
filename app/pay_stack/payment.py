from abc import ABC, abstractmethod
from app.user.user import BusinessUser as b_user


class Payment(ABC):

    @abstractmethod
    def create_user_account():
        """create a sub-account on payment service to represent new customer, for customer payouts and more..."""

    @abstractmethod
    def remove_user_account():
        """Delete user sub-account """

    @abstractmethod
    def initialize_transaction():
        """initialize a new payment"""

    @abstractmethod
    def end_transaction():
        """close a transaction"""


class PayStackPayment(Payment):

    def create_user_account():
        pass

    def remove_user_account():
        pass
    
    def initialize_transaction():
        pass

    def end_transaction():
        pass


