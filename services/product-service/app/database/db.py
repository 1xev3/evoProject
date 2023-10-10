from mongoengine import connect

class MongoDB():
    def __init__(self, mongo_dns):
        connect(host=mongo_dns)