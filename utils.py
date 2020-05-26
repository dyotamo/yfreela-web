from secrets import choice
from faker import Faker
from models import Freela

fake = Faker()

CATEGORIES = [
    'Java', 'Python', 'Rust', 'C++', 'Go', 'Ruby', 'Typescript', 'ES6',
    'Rails', 'Node', 'Deno'
]

FREELAS = []

for index in range(100):
    FREELAS.append(
        Freela(
            index,
            fake.name(),
            fake.city(),
            fake.paragraph(nb_sentences=5),
            fake.email(),
            fake.phone_number(),
            choice(CATEGORIES),
        ))
