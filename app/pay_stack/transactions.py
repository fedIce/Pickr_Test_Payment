from typing import Any
from app.pay_stack.base_setup import Methods, PayStack
from . import utils
import os
from .errors import InvalidDataError


class Transaction:

    def __init__(self, currency=None):
        self.methods = Methods
        self.stack = PayStack()
        if not currency:
            self.CURRENCY = os.getenv('CURRENCY', 'NGN')
        else:
            self.CURRENCY = currency

        if not self.CURRENCY:
            raise InvalidDataError(
                "Currency must be explicitly defined in the .env or passed during a transaction initialization")

    def getall(self, start_date=None, end_date=None, status=None, pagination=10):
        """
        Gets all your transactions

        args:
        pagination -- Count of data to return per call
        from: start date
        to: end date
        """
        url = self.stack._url("/transaction/?perPage={}".format(pagination))
        url = url + "&status={}".format(status) if status else url
        url = url + "&from={}".format(start_date) if start_date else url
        url = url + "&to={}".format(end_date) if end_date else url

        return self.stack._handle_requests(url, self.methods.GET.value)

    def getone(self, transaction_id):
        """
        Gets one customer with the given transaction id

        args:
        Transaction_id -- transaction we want to get
        """
        url = self.stack._url("/transaction/{}/".format(transaction_id))
        return self.stack._handle_requests(url, self.methods.GET.value)

    def totals(self):
        """
        Gets transaction totals
        """
        url = self.stack._url("/transaction/totals/")
        return self.stack._handle_requests(url, self.methods.GET.value)

    def initialize(self, email, amount, split_code=None, plan=None, reference=None, channel=None, metadata=None):
        """
        Initialize a transaction and returns the response

        args:
        email -- Customer's email address
        amount -- Amount to charge
        plan -- optional
        Reference -- optional
        channel -- channel type to use
        metadata -- a list if json data objects/dicts
        """
        amount = utils.validate_amount(amount)
        print(email, amount, split_code, plan)

        if not email:
            raise InvalidDataError("Customer's Email is required for initialization")

        url = self.stack._url("/transaction/initialize")
        payload = {
            "email": email,
            "amount": amount,
        }

        if plan:
            payload.update({"plan": plan})
        if channel:
            payload.update({"channels": channel})
        if reference:
            payload.update({"reference": reference})
        if metadata:
            payload = payload.update({"metadata": {"custom_fields": metadata}})
        if split_code:
            payload.update({"split_code": split_code})

        return self.stack._handle_requests(url, self.methods.POST.value, payload)

    def charge(self, email, auth_code, amount, reference=None, metadata=None):
        """
        Charges a customer and returns the response

        args:
        auth_code -- Customer's auth code
        email -- Customer's email address
        amount -- Amount to charge
        reference -- optional
        metadata -- a list if json data objects/dicts
        """
        amount = utils.validate_amount(amount)

        if not email:
            raise InvalidDataError("Customer's Email is required to charge")

        if not auth_code:
            raise InvalidDataError(
                "Customer's Auth code is required to charge")

        url = self.stack._url("/transaction/charge_authorization")
        payload = {
            "authorization_code": auth_code,
            "email": email,
            "amount": amount,
        }

        if reference:
            payload.update({"reference": reference})
        if metadata:
            payload.update({"metadata": {"custom_fields": metadata}})

        return self.stack._handle_requests(url, self.methods.POST.value, payload)

    def verify(self, reference):
        """
        Verifies a transaction using the provided reference number

        args:
        reference -- reference of the transaction to verify
        """

        reference = str(reference)
        url = self.stack._url("/transaction/verify/{}".format(reference))
        return self.stack._handle_requests(url, self.methods.GET.value)

    def fetch_transfer_banks(self):
        """
        Fetch transfer banks
        """

        url = self.stack._url("/bank")
        return self.stack._handle_requests(url, self.methods.GET.value)

    def create_transfer_customer(self, bank_code, account_number, account_name):
        """
        Create a transfer customer
        """
        url = self.stack._url("/transferrecipient")
        payload = {
            "type": "nuban",
            "currency": self.CURRENCY,
            "bank_code": bank_code,
            "account_number": account_number,
            "name": account_name,
        }
        return self.stack._handle_requests(url, self.methods.POST.value, payload)

    def transfer(self, recipient_code, amount, reason, reference=None):
        """
        Initiates transfer to a customer
        """
        amount = utils.validate_amount(amount)
        url = self.stack._url("/transfer")
        payload = {
            "amount": amount,
            "reason": reason,
            "recipient": recipient_code,
            "source": "balance",
            "currency": self.CURRENCY,
        }
        if reference:
            payload.update({"reference": reference})

        return self.stack._handle_requests(url, self.methods.POST.value, payload)


    def create_transaction_split(self, name: str =None, type: str='percentage', currency: str=None, subaccounts:dict[object]=[], bearer:dict[str, Any]=None):
        """
        Creates a transaction split which returns a split Id which can be used to initialize a split transactions

        name - name of split
        type - split type (percentage | flat)
        currency - currency to payout split
        subaccounts - list of subacounts and split amount objects
        bearer {
            bearer_type - the account who bears charges of transaction ( account | subaccount | all-proportional | all )
            bearer_asubaccount - account_id of bearer
        }
        """
        url = self.stack._url("/split")
        payload = {
            "name": name,
            "type": type,
            "currency": currency,
            "subaccounts": subaccounts,
            "bearer_type": bearer["bearer_type"],
            "bearer_subaccount": bearer["bearer_subaccount"]
        }

        return self.stack._handle_requests(url, Methods.POST.value, payload)

    def verify_transaction(self, ref: str):
        url = self.stack._url(f'transaction/verify/:{ref}')
        return self.stack._handle_requests(url, Methods.GET.value)