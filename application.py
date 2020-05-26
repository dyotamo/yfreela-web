import json
import falcon

from utils import CATEGORIES, FREELAS


class CategoryResource(object):
    def on_get(self, req, resp):
        resp.body = json.dumps([category for category in CATEGORIES])


class CategoryDetailsResource(object):
    def on_get(self, req, resp, name):
        resp.body = json.dumps([
            freela.__dict__ for freela in FREELAS
            if (name.lower() in freela.category.lower())
        ])


class FreelaDetailsResource(object):
    def on_get(self, req, resp, id):
        for freela in FREELAS:
            if freela.id == int(id):
                resp.body = json.dumps(freela.__dict__)
                return
        resp.status = falcon.HTTP_404


application = falcon.API()

application.add_route('/categories', CategoryResource())
application.add_route('/categories/{name}', CategoryDetailsResource())
application.add_route('/freelas/{id}', FreelaDetailsResource())
