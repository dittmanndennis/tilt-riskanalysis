import falcon
import json
import validators as val

from ..common.constants import *
from ..controller.controller import *
from .json_encoder import *

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class TILTResource:

    async def on_get_update(self, req, resp):
        try:
            Controller().update()
            doc = { "SUCCESS": "Database was updated!"}
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except Exception as e:
            doc = { "ERROR": e }
            #doc = JSONEncoder().encode(doc)
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404

    async def on_get_updateDomain(self, req, resp, domain):
        try:
            Controller().updateDomain(domain)
            doc = { "SUCCESS": "Database was updated!"}
        except Exception as e:
            doc = { "ERROR": e }
            #doc = JSONEncoder().encode(doc)
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404

    async def on_get_domain(self, req, resp, domain):
        try:
            if val.domain(domain):
                doc = Controller().getRiskScore(domain)
                if doc["RiskScore"] == None:
                    doc = { "ERROR": "TILT not found" }
                    #doc = JSONEncoder().encode(doc)
                    resp.text = json.dumps(doc, ensure_ascii=False)
                    resp.status = falcon.HTTP_404
                else:
                    #doc = JSONEncoder().encode(doc)
                    resp.text = json.dumps(doc, ensure_ascii=False)
                    resp.status = falcon.HTTP_200
            else:
                doc = { "ERROR": "TILT not found" }
                #doc = JSONEncoder().encode(doc)
                resp.text = json.dumps(doc, ensure_ascii=False)
                resp.status = falcon.HTTP_404
        except Exception as e:
            doc = { "ERROR": e }
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404