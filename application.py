from falcon import API
from resources import (IndexResource, CategoryResource,
                       CategoryDetailsResource, FreelaDetailsResource,
                       SearchResource, LoginResource, SignupResource,
                       UpdatePassword)

application = API()
application.add_route('/', IndexResource())
application.add_route('/categories', CategoryResource())
application.add_route('/categories/{cat_name}', CategoryDetailsResource())
application.add_route('/freelas/{freela_id}', FreelaDetailsResource())
application.add_route('/search/{cat_query}', SearchResource())
application.add_route('/login', LoginResource())
application.add_route('/signup', SignupResource())
application.add_route('/update-password', UpdatePassword())
