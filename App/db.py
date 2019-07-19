# -*- coding: utf-8 -*-
from __future__ import print_function
from pymongo import MongoClient

host = '192.168.28.48'
port = 27017
database = 'autotest'


class UsersCollection:
    def __init__(self):
        self.client = MongoClient(host=host,port=port)
        self.db = self.client.get_database(database)
        self.collection = self.db.get_collection('users')

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()