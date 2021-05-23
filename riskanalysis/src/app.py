import falcon.asgi
import mongoengine as mongo

from .resource.tilt_resource import *
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
    MONGO['DATABASE'],
    host=MONGO['HOST'],
    port=MONGO['PORT'],
    username=MONGO['USERNAME'],
    password=MONGO['PASSWORD'],
    authentication_source=MONGO['AUTHENTICATION_SOURCE']
)

# falcon.API instances are callable WSGI apps
app = falcon.asgi.App()

# things will handle all requests to the '/things' URL path
# 
res = TILTResource()
app.add_route('/', res)