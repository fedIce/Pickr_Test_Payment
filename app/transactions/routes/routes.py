from app import app, request
import json
from app.transactions.controllers.controller import create_split_transaction, create_wallet, new_transaction, verify_transactions


@app.route("/")
def add_sub_account():
    sub = create_wallet(request.get_json())
    return json.dumps(sub)


@app.route("/send", methods=['POST'])
def transaction():
    user = request.get_json(force=True)
    transaction = new_transaction(user)
    return json.dumps(transaction)


@app.route("/create_split")
def new_split():
    data = request.get_json(force=True)
    split = create_split_transaction(data)
    return json.dumps(split)


@app.route("/transaction/verify", methods=['GET'])
def verify_transaction():
    ref = request.args.get("ref")
    return verify_transactions(ref)