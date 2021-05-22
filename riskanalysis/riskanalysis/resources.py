import falcon
import json
import io
import os
import uuid
import mimetypes

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class Resource:

    async def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        doc = {
            'images': [
                {
                    'href': '/home/dennis/Pictures/Depot.png'
                }
            ]
        }
        resp.body = json.dumps(doc, ensure_ascii=False)