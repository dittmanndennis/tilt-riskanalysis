import falcon
import pymongo as pymongo
import re
import json
import uuid

from ..common.constants import *
from ..logic.logic import *

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
tiltCollection = client["RiskAnalysis"]["tilt"]

class TILTResource:

    async def on_get(self, req, resp, domain):
        try:
            print(domain)
            doc = tiltCollection.find_one({ "meta.url": re.compile(domain + "/|" + domain + "$") } )
            if doc == None:
                doc = { "error": "TILT not found" }
                doc = JSONEncoder().encode(doc)
                resp.text = json.dumps(doc, ensure_ascii=False)
                resp.status = falcon.HTTP_404
            else:
                doc = JSONEncoder().encode(doc)
                resp.text = json.dumps(doc, ensure_ascii=False)
                resp.status = falcon.HTTP_200
        except Exception as e:
            print(e)
            doc = { "error": "ERROR" }
            doc = JSONEncoder().encode(doc)
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404

    async def on_post(self, req, resp, user_id):
        #tiltJson = await req.get_media()
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