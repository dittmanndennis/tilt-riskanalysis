import falcon.asgi

from .api.tilt_resource import *

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
app.add_route('/update', res, suffix='update')
app.add_route('/update/{domain}', res, suffix='updateDomain')
app.add_route('/{domain}', res, suffix='domain')
app.add_route('/calculate', res, suffix='calculate')
app.add_route('/calculateRisks', res, suffix='calculateRisks')
app.add_route('/deleteGraph', res, suffix='deleteGraph')
app.add_route('/deleteProperties', res, suffix='deleteProperties')
app.add_route('/deleteCollection/{collection}', res, suffix='deleteCollection')
app.add_route('/generate/{i}', res, suffix='generate')