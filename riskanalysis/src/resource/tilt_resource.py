import falcon
import pymongo as pymongo
import re
import json

from ..common.constants import *
from ..logic.logic import *
from ..logic.json_encoder import *

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
            doc = { "error": e }
            doc = JSONEncoder().encode(doc)
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404