from falcon import HTTP_403, HTTP_404, HTTP_201
from falcon.media.validators import jsonschema
from peewee import IntegrityError

from services import FreelaService, AccountService, HashService

from utils import LOGIN_SCHEMA, SIGNUP_SCHEMA, UPDATE_PASSWORD_SCHEMA
from models import Freela

freela_service = FreelaService()
account_service = AccountService()
hash_service = HashService()


class IndexResource:
    def on_get(self, req, resp):
        resp.media = dict(
            index='/',
            all_categories='/categories',
            category_freelas='/categories/{cat_name}',
            freela_details='/freelas/{freela_id}',
            search_freelas='/search/{cat_query}',
            login='/login',
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


class LoginResource:
    @jsonschema.validate(LOGIN_SCHEMA)
    def on_post(self, req, resp):
        email = req.media['email']
        password = req.media['password']

        try:
            freela = account_service.login(email=email, password=password)
            hash = hash_service.generate_hash(freela.id)

            resp.media = dict(hash=hash, profile=freela.to_json())
        except Freela.DoesNotExist:
            resp.status = HTTP_403
            resp.media = 'Usuário e senha não combinam.'


class SignupResource:
    @jsonschema.validate(SIGNUP_SCHEMA)
    def on_post(self, req, resp):
        try:
            json = req.media
            account_service.create_freela(name=json['name'],
                                          city=json['city'],
                                          bio=json['bio'],
                                          email=json['email'],
                                          phone=json['phone'],
                                          category=json['category'],
                                          password=json['password'])
            resp.status = HTTP_201
        except IntegrityError:
            resp.status = HTTP_403
            resp.media = 'Usuário já cadastrado.'


class UpdateProfile:
    pass


class UpdatePassword:
    @jsonschema.validate(UPDATE_PASSWORD_SCHEMA)
    def on_post(self, req, resp):
        print(req.__dict__)
        # account_service.authenticate(req.media['hash'])
