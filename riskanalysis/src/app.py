import falcon.asgi
import mongoengine as mongo

from .resource.resources import *
from .common.constants import *

# swagger ui - NO ASGI SUPPORT YET
#from falcon_swagger_ui import register_swaggerui_app

# register swagger ui - NO ASGI SUPPORT YET
#register_swaggerui_app(app, SWAGGERUI_URL, SCHEMA_URL, page_title=PAGE_TITLE,
#    favicon_url=FAVICON_URL,
#    config={'supportedSubmitMethods': ['get', 'post']}
#)

# connecting to mongoDB
mongo.connect(
    db=MONGO['DATABASE'],
    host=MONGO['HOST'],
    port=MONGO['PORT'],
    username=MONGO['USERNAME'],
    password=MONGO['PASSWORD']
)

# falcon.API instances are callable WSGI apps
app = falcon.asgi.App()

# things will handle all requests to the '/things' URL path
# 
res = Resource()
app.add_route('/', res)