
# goal of recommendation system:
#  1. guage user's technical ability and interests (front end, back end, etc.)
#  2. get user's company preference for series A or B, location, size
#  3. filter list of companies applicable for user's preferences
#  4. rank remaining companies based on user's technical ability, user's interests, and company viability

import json
from json import dumps, loads
import requests
from user_key import USER_KEY
import pprint

class rec_system:
    def __init__(self):

        # user data
        self.user_pref_series = None
        self.user_pref_location = None
        self.user_pref_size = None
        self.user_profile_keywords = {}

        # company data
        self.companies_data = {}

    def loadUserData(self, json_data):

        # test json parsing code
        json_decode=json.load(json_data)
        for item in json_decode:
            print(item.get('labels').get('en').get('value'))

    def loadCompaniesData(self):
        self.companies_data = {}

        org = 'sequoia-capital'
        request = requests.get(f"https://api.crunchbase.com/v3.1/organizations/{org}/investments?user_key={USER_KEY}")
        j = loads(request.text)

        # pp = pprint.PrettyPrinter(depth=1)
        for company_entry in j['data']['items']:
            # pp.pprint(company_entry)
            name = company_entry['relationships']['funding_round']['relationships']['funded_organization']['properties']['name']
            num_employees_max = company_entry['relationships']['funding_round']['relationships']['funded_organization']['properties']['num_employees_max']
            num_employees_min = company_entry['relationships']['funding_round']['relationships']['funded_organization']['properties']['num_employees_min']
            contact_email = company_entry['relationships']['funding_round']['relationships']['funded_organization']['properties']['contact_email']
            description = company_entry['relationships']['funding_round']['relationships']['funded_organization']['properties']['description']
            funding_series = company_entry['relationships']['funding_round']['properties']['series']
            money_raised = company_entry['relationships']['funding_round']['properties']['money_raised_usd']

            self.companies_data[name] = {'num_employees_min':num_employees_min, 'num_employees_max':num_employees_max,'contact_email':contact_email,'description':description,'funding_series':funding_series,'money_raised':money_raised}
            print(str(name)+", "+str(contact_email))

    def getRankingForCompany(self, company_name):
        rank_sum = 0

        company_data = self.companies_data[company_name]

        return rank_sum

    def rankCompaniesForUser(self):
        company_rankings = []
        for company in self.companies_data:
            company_rankings.append((company, self.getRankingForCompany(company)))

        return sorted(company_rankings, key=lambda x: -x[1])

user_recs = rec_system()
user_recs.loadCompaniesData()
user_recs.loadUserData(open('test_json.json'))
print("RANKINGS: "+str(user_recs.rankCompaniesForUser()))
