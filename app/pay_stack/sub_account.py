

from app.pay_stack.base_setup import Methods, PayStack
from app.pay_stack.errors import InvalidDataError
import os


class SubAccount:
    def __init__(self):
        self.stack = PayStack()
        self.url = self.stack._url("/subaccount")
        self.PERCENTAGE_CHARGE = os.getenv("DEFAULT_PERCENTAGE_CHARGE", None)
        if not self.PERCENTAGE_CHARGE:
            raise InvalidDataError(
                "a value needs to be explicitly defined for a sub-account percentage charge.")

    def add_sub_account(self, account_details):
        """creating a new sub-account for new sellers"""

        if self.sub_account_exists(account_details["account_number"]):
            return "this account already has a subaccount associated with it"
            

        account = {
            u"business_name": account_details[u"business_name"],
            u"settlement_bank": account_details[u"settlement_bank"],
            u"account_number": account_details[u"account_number"],
            u"percentage_charge": account_details[u"percentage_charge"] if u'percentage_charge' in account_details else self.PERCENTAGE_CHARGE,
            u"description": account_details[u"description"]
        }

        return self.stack._handle_requests(self.url, Methods.POST.value, account)

    def list_sub_accounts(self):
        """
        get all sub accounts associated with pickr 
        """
        return self.stack._handle_requests(self.url, Methods.GET.value)

    def get_sub_account(self, id: str):
        """
        get a sub-account
        """
        url = self.url + f'/:{id}'
        return self.stack._handle_requests(url, Methods.GET.value)

    def sub_account_exists(self, account_number):
        accounts = self.list_sub_accounts()
        sub_accounts = accounts[3]
        return [account['account_number'] == account_number for account in sub_accounts][0]

