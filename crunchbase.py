from os import makedirs
from os.path import abspath, join, exists
from json import dumps, loads
import pprint

# 3rd party
import requests
from pycrunchbase import CrunchBase
from user_key import USER_KEY
from tinydb import TinyDB

DB_ROOT = 'db/'
ORG = 'sequoia-capital'

def main():
    if not exists(DB_ROOT):
        makedirs(DB_ROOT, exist_ok=True)

    db = TinyDB(join(DB_ROOT, 'urls_database.json'))
    db.purge_tables()

    # cb = CrunchBase(USER_KEY)
    # investor = cb.organization('sequoia-capital')

    res = requests.get(f'https://api.crunchbase.com/v3.1/organizations/{ORG}/investments?user_key={USER_KEY}')
    j = loads(res.content) # first load of the data

    total_pages = j['data']['paging']['number_of_pages']
    current = 1

    table = db.table(f"{ORG}")
    while current < total_pages:
        for i in j['data']['items']:
            table.insert(i)
        res = requests.get(j['data']['paging']['next_page_url'], params={'user_key':USER_KEY})
        j = loads(res.content)
        current += 1


    # pp = pprint.PrettyPrinter(j, depth=6)

    for i in table:
        print(i)

if __name__ == "__main__":
    main()


# size
# stage
# funding round