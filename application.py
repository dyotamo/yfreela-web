from os import environ
from json import dumps
from hashlib import md5
from falcon import API, HTTP_404
from falcon.media.validators import jsonschema
from jwt import encode, decode

from utils import CATEGORIES
from models import Freela


class CategoryResource(object):
    def on_get(self, req, resp):
        resp.media = [category for category in CATEGORIES]


class CategoryDetailsResource(object):
    def on_get(self, req, resp, name):
        resp.media = [
            freela.to_json() for freela in Freela.select()
            if (freela.category.lower() == name.lower())
        ]


class FreelaDetailsResource(object):
    def on_get(self, req, resp, id):
        try:
            resp.media = Freela[id].to_json
        except Freela.DoesNotExist:
            resp.status = HTTP_404


class SearchResource(object):
    def on_get(self, req, resp, query):
        resp.media = [
            freela.to_json() for freela in Freela.select().where(
                Freela.category.contains(query))
        ]


class LoginResource(object):
    login_schema = {
        "type": "object",
        "properties": {
            "email": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        },
        "required": ["email", "password"]
    }

    @jsonschema.validate(login_schema)
    def on_post(self, req, resp):
        email = req.media['email']
        password = req.media['password']

        try:
            freela = Freela.select().where(
                Freela.email == email and Freela.password == md5(
                    password.encode()).hexdigest()).get()

            resp.body = encode(dict(id=freela.id),
                               environ['SECRET'],
                               algorithm='HS256')
        except Freela.DoesNotExist:
            resp.body = 'Usuário e senha não combinam.'


application = API()

application.add_route('/categories', CategoryResource())
application.add_route('/categories/{name}', CategoryDetailsResource())
application.add_route('/freelas/{id}', FreelaDetailsResource())
application.add_route('/login', LoginResource())
