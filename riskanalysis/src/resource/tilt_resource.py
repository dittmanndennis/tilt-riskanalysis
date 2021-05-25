import falcon
import pymongo as pymongo
import json
import io
import os
import uuid
import mimetypes

from ..common.constants import *

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

# pymongo connecting to mongoDB
client = pymongo.MongoClient(
    #MONGO['DATABASE'],
    host=MONGO['HOST'],
    port=MONGO['PORT'],
    username=MONGO['USERNAME'],
    password=MONGO['PASSWORD']#,
    #authentication_source=MONGO['AUTHENTICATION_SOURCE']
)
tiltCollection = client.RiskAnalysis.tilt

class TILTResource:

    async def on_get(self, req, resp):
        try:
            doc = tiltCollection
        except Exception as e:
            print(e)
            doc = {'images': [{'href': 'https://dittmann.io/'}]}
            resp.text = json.dumps(doc, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp, user_id):
        try:
            doc = req.context.Document
        except AttributeError:
            raise falcon.HTTPBadRequest(
                title='Missing thing',
                description='A thing must be submitted int the request body.'
            )

        proper_thing = await self.db.add_thing(doc)

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])