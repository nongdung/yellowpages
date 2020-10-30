from mongoengine import connect
from ../configs import *

def initMongo():
    return connect(
        db='yellowpages',
        username='admin',
        password='12345678@',
        host='mongodb://admin:qwerty@localhost/production'
    )
