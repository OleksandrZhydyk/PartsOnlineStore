import time


def get_order_id(user_pk):
    timestamp = str(time.time())
    return abs(hash(str(user_pk)+timestamp)) % (10 ** 8)
