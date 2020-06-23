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
        freela = self.get_freela(freela_id)

        if action == 'like':
            like_or_dislike, created = Like.get_or_create(freela=freela,
                                                          device_id=device_id)

            # Não pode dar like e deslike ao mesmo tempo, então depois de dar like deve remover o dislike, se existir...
            if self.disliked(freela, device_id):
                Dislike.get(freela=freela,
                            device_id=device_id).delete_instance()

        elif action == 'dislike':
            like_or_dislike, created = Dislike.get_or_create(
                freela=freela, device_id=device_id)

            if self.liked(freela, device_id):
                Like.get(freela=freela, device_id=device_id).delete_instance()

        # Se o like ou dislike sempre existiu
        if created == False:
            like_or_dislike.delete_instance()

        return self.get_freela(freela_id)

    def liked(self, freela, device_id):
        return Like.get_or_none(freela=freela, device_id=device_id) is not None

    def disliked(self, freela, device_id):
        return Dislike.get_or_none(freela=freela,
                                   device_id=device_id) is not None
