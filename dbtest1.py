import pymongo
from mongoengine import *
import json
#import dnspython

#connect("Senior-Design-Project", host='mongodb+srv://dduckworth:x2FXe?7J@senior-design-project.xpkmu.mongodb.net/test?authSource=admin&replicaSet=atlas-q1uqgf-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')

# Defining Documents

class metaData(Document):
    transmitter_mode = StringField(required= True)
    status = StringField(required= True)
    Id = IntField()
    waterfall = StringField()
    user_verified_status = StringField()


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

# Saving a doc test

# metaData = metaData(
#     transmitter_mode = "DUV",
#     status = "Bad",
#     Id = 152,
#     waterfall = "null"
# ).save()

print("done")