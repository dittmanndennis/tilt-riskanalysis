import falcon
import msgpack

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        doc = {
            'images': [
                {
                    'href': '/home/dennis/Pictures/Depot.png'
                }
            ]
        }
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK

class ResourceTwo(object):
    def on_get(self, req, resp):
        resp.body = "Test successful"

class ResourceThree(object):
    def on_get(self, req, resp):
        resp.body = "also successful"