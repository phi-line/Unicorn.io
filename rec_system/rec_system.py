
# goal of recommendation system:
#  1. guage user's technical ability and interests (front end, back end, etc.)
#  2. get user's company preference for series A or B, location, size
#  3. filter list of companies applicable for user's preferences
#  4. rank remaining companies based on user's technical ability, user's interests, and company viability

import re
import math
import json
from json import dumps, loads
import requests
from user_key import USER_KEY
import pprint

industry_keywords = {
  "big data": ["scalable", "scalability", "big", "data", "sql", "mongodb", "python","cloud", \
    "mining", "database","aws","gcp","global","expand","ai","intelligen","learn"],
  "software": ["object","oriented","system","design","scalable","database","systems", \
    "object-oriented","algorithm","software","debugging","debug","architecture", \
    "java","python","c++","application","algorithms","stack","app","vision","learn","algorithm"],
  "web": ["es6","es5","eslint","javascript","typescript","ajax","react","reactjs", \
    "angular","angularjs","http","web","website","websites","node","js","html","css","nodejs","interface"],
  "mobile": ["ios","android","objective-c","native","swift","mobile","accessib","phone","app"],
  "hardware": ["arduino","matlab","raspberry","c","c++","pspice","autodesk","cad","solidworks", \
    "circuit","circuitlab","signal","hardware","drone","device","sensor","processor","chip"],
  "security": ["cyber","security","defense","operating","kernel","thread","process","flag","cft","threat"],
  "finance": ["cryptocurrency","bitcoin","blockchain","trading","quant","ether","coin","asset"]
}

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

        # test user
        self.user_pref_size = 50
        self.user_pref_location = 'CA'
        self.user_pref_series = 'B'
        self.user_profile_keywords = {'big data': 1.0, 'software': 0.0}

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

    def getRankingForCompany(self, company_name):
        rank_sum = 0

        company_data = self.companies_data[company_name]

        # creates word frequency vector for company description
        description = company_data['description']
        freq_vec_company = {}

        if description != None:
            clean_description = re.sub('[^a-z0-9- ]', ' ', description.lower())
            tokens = clean_description.split()
            for t in tokens:
                for k,v in industry_keywords.items():
                    if t in v:
                        freq_vec_company[k] = freq_vec_company.get(k, 0) + 1
            sum_vals = sum(freq_vec_company.values())
            for k, v in freq_vec_company.items():
                freq_vec_company[k] = v * 1.0 / sum_vals

        freq_vec_user = self.user_profile_keywords

        # calculates difference between company and user keyword vectors
        for key in industry_keywords:
            value_company = 1.0
            value_user = 0.0
            if key in freq_vec_company:
                value_company = freq_vec_company[key]
            if key in freq_vec_user:
                value_user = freq_vec_user[key]

            rank_sum += math.fabs(value_company-value_user)

        # changes rating based on user preference for size
        if company_data['num_employees_max'] != None and company_data['num_employees_min'] != None:
            if self.user_pref_size <= company_data['num_employees_max'] and self.user_pref_size >= company_data['num_employees_min']:
                rank_sum = rank_sum*0.75

        # changes rating based on user preference for series
        if company_data['funding_series'] != None:
            value_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
            if math.fabs(value_map[company_data['funding_series']]-value_map[self.user_pref_series]) == 0:
                rank_sum = rank_sum*0.8
            elif math.fabs(value_map[company_data['funding_series']]-value_map[self.user_pref_series]) == 1:
                rank_sum = rank_sum*0.925

        return rank_sum

    def rankCompaniesForUser(self):
        company_rankings = []
        for company in self.companies_data:
            company_rankings.append((company, self.getRankingForCompany(company)))

        return sorted(company_rankings, key=lambda x: x[1])

user_recs = rec_system()
user_recs.loadCompaniesData()
user_recs.loadUserData(open('test_json.json'))
print("TOP 10 RANKINGS: "+str(user_recs.rankCompaniesForUser()[:10]))
