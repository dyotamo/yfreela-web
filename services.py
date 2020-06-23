from os import environ

from utils import CATEGORIES
from models import Freela, Like, Dislike


class FreelaService:
    def get_categories(self):
        return CATEGORIES

    def get_freelas(self, cat_name):
        return Freela.select().where(Freela.category == cat_name)

    def get_freela(self, freela_id):
        return Freela[freela_id]

    def search_freela(self, cat_query):
        return Freela.select().where(Freela.category.contains(cat_query))

    def like_or_dislike_freela(self, freela_id, device_id, action):
        if action == 'like':
            like_or_dislike, created = Like.get_or_create(
                freela=self.get_freela(freela_id), device_id=device_id)
        elif action == 'dislike':
            like_or_dislike, created = Dislike.get_or_create(
                freela=self.get_freela(freela_id), device_id=device_id)

        if created:
            return self.get_freela(freela_id)
        else:
            like_or_dislike.delete_instance()
            return self.get_freela(freela_id)

    def liked(self, freela, device_id):
        return Like.get_or_none(freela=freela, device_id=device_id) is not None

    def disliked(self, freela, device_id):
        return Dislike.get_or_none(freela=freela,
                                   device_id=device_id) is not None
