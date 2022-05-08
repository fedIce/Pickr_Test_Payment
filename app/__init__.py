from flask import Flask, request
from app.Observer.log.transaction_log_listerner import setup_transaction_log_event_handlers
from app.Observer.log.users_log_listener import setup_users_log_event_handlers
from dotenv import load_dotenv
from flask_cors import CORS



load_dotenv()

setup_transaction_log_event_handlers()
setup_users_log_event_handlers()

app = Flask(__name__)
CORS(app, supports_credentials=True)



from app.transactions.routes import routes
from app.Database import playground_tests 



