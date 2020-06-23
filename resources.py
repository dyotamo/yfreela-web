from falcon import HTTP_403, HTTP_404, HTTP_201
from falcon.media.validators import jsonschema
from peewee import IntegrityError

from services import FreelaService

from models import Freela

freela_service = FreelaService()


class IndexResource:
    def on_get(self, req, resp):
        resp.media = dict(
            index='/',
            all_categories='/categories',
            category_freelas='/categories/{cat_name}',
            freela_details='/freelas/{freela_id}',
            search_freelas='/search/{cat_query}',
        )


class CategoryResource:
    def on_get(self, req, resp):
        resp.media = [cat for cat in freela_service.get_categories()]


class CategoryDetailsResource:
    def on_get(self, req, resp, cat_name):
        resp.media = [
            freela.to_json() for freela in freela_service.get_freelas(cat_name)
        ]


class FreelaDetailsResource:
    def on_get(self, req, resp, freela_id):
        try:
            resp.media = freela_service.get_freela(freela_id).to_json()
        except Freela.DoesNotExist:
            resp.status = HTTP_404


class SearchResource:
    def on_get(self, req, resp, cat_query):
        resp.media = [
            freela.to_json()
            for freela in freela_service.search_freela(cat_query)
        ]