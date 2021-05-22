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
                    'href': 'https://dittmann.io/'
                }
            ]
        }
        resp.body = json.dumps(doc, ensure_ascii=False)

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