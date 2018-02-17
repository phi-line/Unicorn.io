
# goal of recommendation system:
#  1. guage user's technical ability and interests (front end, back end, etc.)
#  2. get user's company preference for series A or B, location, size
#  3. filter list of companies applicable for user's preferences
#  4. rank remaining companies based on user's technical ability, user's interests, and company viability

import json
import requests

class rec_system:
    def __init__(self):

        # user data
        self.user_pref_series = None
        self.user_pref_location = None
        self.user_pref_size = None
        self.user_profile_keywords = [:]

        # company data
        self.companies_data = [:]

    def loadUserData(self, json_data):

        # test json parsing code
        json_decode=json.load(json_data)
        for item in json_decode:
            print(item.get('labels').get('en').get('value'))

    def loadCompaniesData(self):
        self.companies_data = [:]

    def getRankingForCompany(self, company_name):
        rank_sum = 0

        

        return rank_sum

    def rankCompaniesForUser(self):
        company_rankings = []
        for company in self.companies_data:
            company_rankings.append((company, getRankingForCompany))

        return company_rankings

# user_recs = rec_system(open('test_json.json', 'r'))