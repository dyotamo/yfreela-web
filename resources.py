from falcon import HTTP_403, HTTP_404, HTTP_201
from falcon.media.validators import jsonschema
from peewee import IntegrityError

from services import FreelaService
from models import Freela
from utils import LIKE_OR_DISLIKE_SCHEMA

freela_service = FreelaService()


class IndexResource:
    def on_get(self, req, resp):
        resp.media = dict(
            index='/',
            all_categories='/categories',
            category_freelas='/categories/{cat_name}',
            freela_details='/freelas/{freela_id}',
            search_freelas='/search/{cat_query}',
            like_or_dislike='/like_or_dislike',
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
            device_id = req.params.get('device_id')
            freela = freela_service.get_freela(freela_id)

            if device_id:
                json = freela.to_json()
                json['liked'] = freela_service.liked(freela, device_id)
                json['disliked'] = freela_service.disliked(freela, device_id)

                resp.media = json
            else:
                resp.media = freela.to_json()
        except Freela.DoesNotExist:
            resp.status = HTTP_404


class SearchResource:
    def on_get(self, req, resp, cat_query):
        resp.media = [
            freela.to_json()
            for freela in freela_service.search_freela(cat_query)
        ]


class LikeOrDislikeResource:
    @jsonschema.validate(LIKE_OR_DISLIKE_SCHEMA)
    def on_post(self, req, resp):
        freela_id = req.media['freela_id']
        device_id = req.media['device_id']
        action = req.media['action']

        try:
            freela = freela_service.like_or_dislike_freela(
                freela_id, device_id, action)

            json = freela.to_json()
            json['liked'] = freela_service.liked(freela, device_id)
            json['disliked'] = freela_service.disliked(freela, device_id)

            resp.media = json
        except Freela.DoesNotExist:
            resp.status = HTTP_404