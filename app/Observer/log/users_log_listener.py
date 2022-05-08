from app.Observer import event
from app.Observer.log.log import log_event

def user_created_log(data):
    log_event(f"A new user account was created for {data[u'firstname']} {data[u'lastname']} with email {data[u'email']}")



def setup_users_log_event_handlers():
    event.subscribe("user_created_log_event", user_created_log)