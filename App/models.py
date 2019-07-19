# -*- coding: utf-8 -*-
from __future__ import print_function
from mongoengine import  Document,DateTimeField,StringField,IntField ,connect
from datetime import datetime
from App.db import host,port,database,UsersCollection

connect(database,host=host,port=port)

#TODO: find  save delete
class Users(Document):
    username = StringField()
    password = StringField(default='it789123')
    level = IntField(default=0)
    insert_time = DateTimeField(default=datetime.now())

    def save_it(self):
        with UsersCollection as uc:
            result = uc.find_one({'username':self.username})
            if not result:
                self.save()
                return
            print("{} 数据已存在".format(self.username))

    def __str__(self):
        return '{}\n{}\n{}\n{}'.format(self.username,self.password,self.level,self.insert_time)