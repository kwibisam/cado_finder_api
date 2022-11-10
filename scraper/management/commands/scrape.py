from django.core.management.base import BaseCommand
from base import models
import json
import requests
import time
import os

class Command(BaseCommand):
    help = "collect advocates"

    TOKEN = os.getenv('API_TOKEN', 'Optional default value')
    page_count = 20
    current_page = 6
    headers = {'Authorization': "Bearer {}".format(TOKEN)}

    advocate_list = []
    company_names = []
    company_list = []
    
    def handle(self, *args, **options):
        while self.current_page < self.page_count:
            BASE_URL = f"https://api.twitter.com/1.1/users/search.json?q=developer advocate&page={self.current_page}"
            print('collecting advocates')
            self.scrap(BASE_URL)
            print('collecting companies')
            self.scrap_comps(self.company_names)
            print("creating companies")
            self.createCompany()
            print("creating advocates",len(self.advocate_list)) 
            self.createAdovocate()
            self.current_page += 1
        self.stdout.write( 'task complete' )

    def createCompany(self):
        for comp in self.company_list:
            name = comp['name']
            bio = comp['bio']
            profile_img = comp['profile_img']
            location = comp['location']
            url = comp['url']
            try:
                models.Company.objects.create(
                    name = name,
                    bio = bio,
                    profile_img = profile_img,
                    location = location,
                    url = url
                )
                print('%s added',name)
            except:
                print('%s already exists' % (name,))

    def createAdovocate(self):
        for advocate in self.advocate_list:
            name = advocate['name']
            username =advocate['username']
            bio = advocate['bio']
            profile_pic = advocate['profile_pic']
            twitter = advocate['twitter']
            comp_name = advocate['company']
            try:
                company = models.Company.objects.filter(name=comp_name).first()
                models.Advocate.objects.create(
                    company = company,
                    name = name,
                    username = username,
                    bio = bio,
                    profile_pic = profile_pic,
                    twitter = twitter,
                )
                print('%s added' %(name))
            except Exception as e:
                print('%s already exists' % (username,))

    def find_comp_name(self,bio):
        bio_terms = bio.lower().split()
        for i in range(len(bio_terms) -1):
            if (bio_terms[i] == 'developer'  or"developer" in bio_terms[i]) and (bio_terms[i+1] == 'advocate' or "advocate" in bio_terms[i+1]):
                if i+3 < len(bio_terms):
                    if bio_terms[i+2].startswith("@") and len(bio_terms[i+2]) >1:
                        #save company name
                        name = bio_terms[i+2].replace('@','').replace('.','')
                        self.company_names.append(name)
                        return name
                    elif bio_terms[i+3].startswith("@") and len(bio_terms[i+3])>1:
                        #save company name
                        name = bio_terms[i+2].replace('@','').replace('.','')
                        self.company_names.append(name)
                        return name
    #collect companies
    def scrap_comps(self, names):
        for name in names:
            url = f"https://api.twitter.com/1.1/users/lookup.json?screen_name={name}"
            try:
                r = requests.get(url, headers=self.headers)
                print(r.status_code)
                data = json.loads(r.content)[0]
                company = {
                    'name': name,
                    'bio': data['description'],
                    'profile_img': data['profile_image_url_https'],
                    'location':data['location'],
                    'url': data['url']
                }
                self.company_list.append(company)
            except Exception as e:
                print('scraping failed with the following exception:')
                print(e)
            time.sleep(40)

    # collect advocates
    def scrap (self, url_):
        try:
            r = requests.get(url_, headers=self.headers)
            data = json.loads(r.content)
            for dict in data:
                profile_pic = dict['profile_image_url_https']
                username = dict['screen_name']
                name = dict['name']
                bio = dict['description']
                twitter= f"https://twitter.com/{username}"
                company = self.find_comp_name(bio)
                advocate = {
                    'name': name,
                    'username': username,
                    'bio': bio,
                    'profile_pic': profile_pic,
                    'twitter': twitter,
                    'company': company
                }
                self.advocate_list.append(advocate)
        except Exception as e:
            print('scraping failed with the following exception:')
            print(e)


