from json import dumps
from falcon import API, HTTP_404

from utils import CATEGORIES
from models import Freela


class CategoryResource(object):
    def on_get(self, req, resp):
        resp.body = dumps([category for category in CATEGORIES])


class CategoryDetailsResource(object):
    def on_get(self, req, resp, name):
        resp.body = dumps([
            freela.to_json() for freela in Freela.select()
            if (freela.category.lower() == name.lower())
        ])


class FreelaDetailsResource(object):
    def on_get(self, req, resp, id):
        try:
            resp.body = dumps(Freela[id].to_json())
        except Freela.DoesNotExist:
            resp.status = HTTP_404


class SearchResource(object):
    def on_get(self, req, resp, query):
        resp.body = dumps([
            freela.to_json() for freela in Freela.select().where(
                Freela.category.contains(query))
        ])


application = API()

application.add_route('/categories', CategoryResource())
application.add_route('/categories/{name}', CategoryDetailsResource())
application.add_route('/freelas/{id}', FreelaDetailsResource())
application.add_route('/search/{query}', SearchResource())
