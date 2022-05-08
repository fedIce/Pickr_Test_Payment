from typing import Any

from flask import request
from app.Observer.event import post_event
from app.helper import extract_value, validate_missing_keys
from app.pay_stack.sub_account import SubAccount
from app.pay_stack.transactions import Transaction
import json

transaction = Transaction()
sub_account = SubAccount()


def new_transaction(user: dict[str, Any]):
    try:
        post_event("payment_initialized_log_event", user)

        split_code = extract_value(user, 'split_code')
        plan = extract_value(user, 'plan')
        reference = extract_value(user, 'reference')
        channel = extract_value(user, 'channel') 
        metadata = extract_value(user, 'metadata')

        amount = float(user['amount'])

        result = transaction.initialize(email=user['email'], amount=amount, split_code=split_code , plan= plan, reference = reference, metadata=metadata, channel=channel)
        # SPL_Sksfukz2Dn
        post_event("payment_successful_log_event", user)
        return result
    except Exception as e:
        post_event("payment_failed_log_event", user)

def create_split_transaction(data: dict[str, Any]):
    name = extract_value(data, 'name')
    type = extract_value(data, 'type')
    currency = extract_value(data, 'currency')
    sub_accounts = extract_value(data, 'sub_account'),
    bearer = extract_value(data, 'bearer')

    split = transaction.create_transaction_split(name=name,type=type, currency=currency, subaccounts=sub_accounts, bearer=bearer)
    return split

def create_wallet(data:dict[str, Any]):
    keys = ['business_name','settlement_bank','account_number','description']
    accnt = sub_account.add_sub_account(validate_missing_keys(data, keys ))
    return json.dumps(accnt)

def verify_transactions(ref):
    return transaction.verify_transaction(ref)
