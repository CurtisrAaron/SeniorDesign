import pymongo
from mongoengine import *
import json

# Defining Documents

class MetaData(Document):
    transmitter_mode = StringField(required= True)
    status = StringField(required= True)
    Id = IntField()
    waterfall = StringField()
    user_vetted_status = StringField(default = 'not vetted')
    model_vetted_status = StringField(default = 'not vetted')


    def json(self):
        metaData_dict = {
            "Id" : metaData.Id,
            "transmitter_mode": metaData.transmitter_mode,
            "status": metaData.status 
        }
        return json.dumps(metaData_dict)
    
    meta = {
        "indexes": ["status", "Id"]
    }
