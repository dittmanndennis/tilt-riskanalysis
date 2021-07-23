import falcon
import json

from ..common.constants import *
from ..controller.controller import *
from .json_encoder import *

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class TILTResource:

    async def on_get(self, req, resp, domain):
        try:
            if len(domain)>0:
                controller = Controller()
                doc = controller.getRiskScore(domain)
                if doc == None:
                    doc = { "error": "TILT not found" }
                    #doc = JSONEncoder().encode(doc)
                    resp.text = json.dumps(doc, ensure_ascii=False)
                    resp.status = falcon.HTTP_404
                else:
                    #doc = JSONEncoder().encode(doc)
                    resp.text = json.dumps(doc, ensure_ascii=False)
                    resp.status = falcon.HTTP_200
            else:
                doc = { "error": "TILT not found" }
                doc = JSONEncoder().encode(doc)
                resp.text = json.dumps(doc, ensure_ascii=False)
                resp.status = falcon.HTTP_404
        except Exception as e:
            doc = { "error": e }
            #doc = JSONEncoder().encode(doc)
            resp.text = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_404