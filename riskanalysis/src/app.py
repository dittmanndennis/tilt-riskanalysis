import falcon.asgi

import pymongo as pymongo
from pymongo.errors import ConnectionFailure

from pprint import pprint

from .resource.tilt_resource import *
from .common.constants import *

from .tilt import *

# swagger ui - NO ASGI SUPPORT YET
#from falcon_swagger_ui import register_swaggerui_app

# register swagger ui - NO ASGI SUPPORT YET
#register_swaggerui_app(api, SWAGGERUI_URL, SCHEMA_URL, page_title=PAGE_TITLE,
    #favicon_url=FAVICON_URL,
#    config={'supportedSubmitMethods': ['get', 'post']}
#)

# falcon.asgi.APP instances are callable ASGI apps
app = falcon.asgi.App()

# 
res = TILTResource()
app.add_route('/{domain}', res)