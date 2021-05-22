import falcon.asgi

from .resources import *

# falcon.API instances are callable WSGI apps
app = falcon.asgi.App()

# things will handle all requests to the '/things' URL path
# 
res = Resource()
app.add_route('/', res)



#help(falcon.API.__call__)
#Help on function __call__ in module falcon.api:
#__call__(self, env, start_response)
#    WSGI `app` method.   
#    Makes instances of API callable from a WSGI server. May be used to
#    host an API or called directly in order to simulate requests when
#    testing the API.    
#    (See also: PEP 3333)    
#    Args:
#        env (dict): A WSGI environment dictionary
#        start_response (callable): A WSGI helper function for setting
#            status and headers on a response.