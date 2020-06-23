from os import environ

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
