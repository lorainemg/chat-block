import json

from threading import Lock
lock = Lock() # External Locker

import requests
def broadcast(message):
    #requests.post("http://127.0.0.1:9443/api", params={'method': 'SENDBLOCK', 'block': message})
    m = json.loads(message)
    if len(m["content"]):
        print(message)

def firsts(collection, limit):
    if len(collection) <= limit:
        return collection[0:limit]
    return collection