
# goal of recommendation system:
#  1. guage user's technical ability and interests (front end, back end, etc.)
#  2. get user's company preference for series A or B, size
#  3. filter list of companies applicable for user's preferences
#  4. rank remaining companies based on user's technical ability, user's interests, and company viability

import re
import math
import json
from json import dumps, loads
import requests

with open('keywords.json', 'r') as f:
  industry_keywords = json.load(f)
  f.close()

class rec_system:
    def __init__(self, user_pref_size=55, \
        user_pref_series='A', user_profile_keywords={}):

        # user data
        self.user_pref_series = user_pref_series
        self.user_pref_size = user_pref_size
        self.user_profile_keywords = user_profile_keywords

        self.companies_data = {}

    def loadCompaniesData(self):
        self.companies_data = {}

        request = requests.get(f"http://127.0.0.1:5000/all")
        j = loads(request.text)

        for company_entry in j:
            name = company_entry['name']
            self.companies_data[name] = company_entry

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
            difference = 1.0

            if key in freq_vec_company:
                if key in freq_vec_user:
                    difference = math.fabs(freq_vec_company[key]-freq_vec_user[key])
                else:
                    difference = math.fabs(freq_vec_company[key])
            elif key in freq_vec_user:
                    difference = math.fabs(freq_vec_user[key])

            rank_sum += difference

        # changes rating based on user preference for size
        if company_data['num_employees_max'] != None and company_data['num_employees_min'] != None:
            if self.user_pref_size <= company_data['num_employees_max'] and self.user_pref_size >= company_data['num_employees_min']:
                rank_sum = rank_sum*0.75
            elif self.user_pref_size < company_data['num_employees_max']*0.5:
                rank_sum = rank_sum*1.25

        # changes rating based on user preference for series
        if company_data['series'] != None:
            value_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
            if math.fabs(value_map[company_data['series']]-value_map[self.user_pref_series]) == 0:
                rank_sum = rank_sum*0.8
            elif math.fabs(value_map[company_data['series']]-value_map[self.user_pref_series]) == 1:
                rank_sum = rank_sum*0.925

        return rank_sum

    def rankCompaniesForUser(self):
        company_names = []
        company_rankings = []

        for company in self.companies_data:
            sizeString = "Unknown size"
            if self.companies_data[company]['num_employees_min'] != None and self.companies_data[company]['num_employees_max'] != None:
                sizeString = str(self.companies_data[company]['num_employees_min'])+" - "+str(self.companies_data[company]['num_employees_max'])+" employees"
            emailString = "No contact email provided"
            if self.companies_data[company]['email'] != None:
                emailString = self.companies_data[company]['email']

            if company not in company_names:
                company_names.append(company)
                company_rankings.append((company,
                                         self.getRankingForCompany(company),
                                         emailString,
                                         sizeString,
                                         None,
                                         self.companies_data[company]['short_description'],
                                         self.companies_data[company]['profile_image_url'],
                                         sizeString,
                                         self.companies_data[company]['url']))
        results = sorted(company_rankings, key=lambda x: x[1])
        return results[:12]
