from os import makedirs
from os.path import abspath, join, exists
from json import dumps, loads
from collections import namedtuple
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

    db = TinyDB(join(DB_ROOT, 'database.json'))
    db.purge_tables()

    # cb = CrunchBase(USER_KEY)
    # investor = cb.organization('sequoia-capital')

    res = requests.get(f'https://api.crunchbase.com/v3.1/organizations/{ORG}/investments?user_key={USER_KEY}')
    j = loads(res.content) # first load of the data

    total_pages = j['data']['paging']['number_of_pages']
    current = 1

    Data = namedtuple('Data', ['name',
                               'description',
                               'email',
                               'num_employees_max',
                               'num_employees_min',
                               'money_raised_usd',
                               'series'])
    

    table = db.table(f"{ORG}")
    while current < total_pages:
        for i in j['data']['items']:
            d = Data(i['relationships']['funding_round']['relationships']['funded_organization']['properties']['name'],
                     i['relationships']['funding_round']['relationships']['funded_organization']['properties']['description'],
                     i['relationships']['funding_round']['relationships']['funded_organization']['properties']['contact_email'],
                     i['relationships']['funding_round']['relationships']['funded_organization']['properties']['num_employees_max'],
                     i['relationships']['funding_round']['relationships']['funded_organization']['properties']['num_employees_min'],
                     i['relationships']['funding_round']['properties']['money_raised_usd'],
                     i['relationships']['funding_round']['properties']['series'])
            table.insert(d._asdict())
            print(d)
        res = requests.get(j['data']['paging']['next_page_url'], params={'user_key': USER_KEY})
        j = loads(res.content)
        current += 1

    # pp = pprint.PrettyPrinter(j, depth=6)


if __name__ == "__main__":
    main()