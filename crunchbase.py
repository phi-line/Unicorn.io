from pycrunchbase import CrunchBase
from user_key import USER_KEY
import pprint

from json import dumps, loads

cb = CrunchBase(USER_KEY)
investor = cb.organization('sequoia-capital')

import requests

req = requests.get(f'https://api.crunchbase.com/v3.1/organizations?user_key={USER_KEY}')
j = loads(req.text)

pp = pprint.PrettyPrinter(depth=6)

for i in j['data']['items']:
    pp.pprint(i)

# size
# stage
# funding round