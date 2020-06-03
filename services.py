from os import environ

from hashlib import md5
from jwt import encode, decode

from utils import CATEGORIES
from models import Freela


class FreelaService:
    def get_categories(self):
        return CATEGORIES

    def get_freelas(self, cat_name):
        return Freela.select().where(Freela.category == cat_name)

    def get_freela(self, freela_id):
        return Freela[freela_id]

    def search_freela(self, cat_query):
        return Freela.select().where(Freela.category.contains(cat_query))


class AccountService:
    def login(self, email, password):
        return Freela.select().where((Freela.email == email)
                                     & (Freela.password == HashService.
                                        encrypt_password(password))).get()

    def authenticate(self, hash):
        print(decode(hash, environ['SECRET'], algorithms=['HS256']))

    def create_freela(self, name, city, bio, email, phone, category, password):
        freela = Freela(name=name,
                        city=city,
                        bio=bio,
                        email=email,
                        phone=phone,
                        category=category)
        freela.password = HashService.encrypt_password(password)
        freela.save()

    def update_freela(self):
        pass


class HashService:
    def generate_hash(self, freela_id):
        return encode(dict(id=freela_id), environ['SECRET'],
                      algorithm='HS256').decode()

    @staticmethod
    def encrypt_password(password):
        return md5(password.encode()).hexdigest()