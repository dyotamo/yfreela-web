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
    email = CharField()
    phone = CharField()
    category = CharField()
    password = CharField()

    def to_json(self):
        return self.__dict__['__data__'].pop('password')

    class Meta:
        database = db


def _generate_fake():
    FAKE = Faker()
    for index in range(1):
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
    print('Starting faking data at {}'.format(datetime.now()))
    _generate_fake()
    print('Finished faking at {}'.format(datetime.now()))
