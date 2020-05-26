from json import loads


def process(element):
    return element['item']['name']


with open('result.txt', 'w') as out:
    out.write('CATEGORIES = [')
    with open('pl.json', 'r') as in_:
        json = loads(in_.read())
        for pl in map(process, json['itemListElement']):
            out.write('"{}",'.format(pl))
    out.write(']')
