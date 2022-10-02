from admin import process_admin
from consumer import process_consumer

def __main__():
    is_admin = False
    is_consumer = False
    if is_admin:
        process_admin()
    elif is_consumer:
        process_consumer()


__main__()
