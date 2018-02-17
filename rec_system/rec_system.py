
# goal of recommendation system:
#  1. guage user's technical ability and interests (front end, back end, etc.)
#  2. get user's company preference for series A or B, location, size
#  3. filter list of companies applicable for user's preferences
#  4. rank remaining companies based on user's technical ability, user's interests, and company viability

import json

class rec_system:
    def __init__(self, json_data):
        json_decode=json.load(json_data)
        for item in json_decode:
            print(item.get('labels').get('en').get('value'))

user_recs = rec_system(open('test_json.json', 'r'))