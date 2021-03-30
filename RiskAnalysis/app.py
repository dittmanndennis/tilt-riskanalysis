import falcon

from .images import *

# falcon.API instances are callable WSGI apps
api = application = falcon.API()

# Resources are represented by long-lived class instances
images = Resource()
things = ResourceTwo()
test = ResourceThree()

# things will handle all requests to the '/things' URL path
api.add_route('/images', images)
api.add_route('/things', things)
api.add_route('/test', test)



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