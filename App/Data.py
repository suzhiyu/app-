from pymongo  import MongoClient
from mongoengine import  Document,DateTimeField,StringField,IntField ,connect
from datetime import datetime


mongo_url = "mongodb://192.168.28.48:27017"
database = 'autotest'
connect(database,host='192.168.28.48',port=27017)

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


class UsersCollection:
    def __init__(self):
        self.mongo_url = mongo_url
        self.client = MongoClient(self.mongo_url)
        self.db = self.client.get_database(database)
        self.collection = self.db.get_collection('users')

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()



if __name__ =="__main__":
    # Users(username='17635241345',level='1').save()
    with UsersCollection() as uc:
        result = uc.find_one_and_update({'username':'17635241345'},update={"$set":{'level':1}})
        print(result)







