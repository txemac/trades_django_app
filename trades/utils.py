import string
import random


__author__ = 'josebermudez'


def id_generator():
    hash_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
    return 'TR{hash}'.format(hash=hash_key)
