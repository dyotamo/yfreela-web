from os import environ
from hashlib import md5
from peewee import (
    PostgresqlDatabase,
    SqliteDatabase,
    Model,
    CharField,
)

from faker import Faker
from secrets import choice
from utils import CATEGORIES
from dsnparse import parse

if environ.get('DATABASE_URL'):
    url = parse(environ.get('DATABASE_URL'))
    db = PostgresqlDatabase(url.path.replace('/', ''),
                            user=url.username,
                            password=url.password,
                            host=url.host,
                            port=url.port)
else:
    db = SqliteDatabase('freela.db')


class Freela(Model):
    name = CharField()
    city = CharField()
    bio = CharField(max_length=1500)
    email = CharField(unique=True)
    phone = CharField()
    category = CharField()
    password = CharField()

    def to_json(self):
        map = self.__dict__['__data__']
        map.pop('password')
        return map

    def __str__(self):
        return self.name

    class Meta:
        database = db


def _generate_fake():
    FAKE = Faker()
    for index in range(100):
        Freela.create(name=FAKE.name(),
                      city=FAKE.city(),
                      bio=FAKE.paragraph(nb_sentences=5),
                      email=FAKE.email(),
                      phone=FAKE.phone_number(),
                      category=choice(CATEGORIES),
                      password=md5(b'admin').hexdigest())


if __name__ == "__main__":
    from datetime import datetime
    db.create_tables([Freela])
