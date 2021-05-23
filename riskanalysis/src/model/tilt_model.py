import mongoengine as mongo

class TILT(mongo.Document):
    id = mongo.StringField()
    price = mongo.FloatField()