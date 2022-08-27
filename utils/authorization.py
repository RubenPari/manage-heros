import hashlib
import os
from random import random

"""
generate a string containing
auth param for use endpoints
"""
def get_params():
    url = ''

    # generate random number for ts param
    ts = str(random.randint(1, 1000))

    url += '?' + ts + '&'

    # get private and public key
    public_key = os.getenv('PUBLIC_KEY')
    private_key = os.getenv('PRIVATE_KEY')

    # generate md5 hash of ts+privatekey+publickey
    hash = hashlib.md5(
        (ts + private_key + public_key).encode('utf-8')).hexdigest()

    url += 'apikey=' + public_key + '&hash=' + hash

    return url
