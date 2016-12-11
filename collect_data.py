
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
import requests
from requests_oauthlib import OAuth1
import argparse
import json
from time import gmtime, strftime
import os
import glob
import time


# In[2]:

listings = pd.read_csv(r'data\boston-airbnb-open-data\listings.csv')

neighbourhood = pd.read_csv(r'data\boston-airbnb-open-data\neighbourhoods.csv')

print(listings.head())
print(neighbourhood.head())


# # Data Scrubbing

# In[14]:

print("Shape of this dataframe.{val}".format(val=listings.shape))

pd.DataFrame(listings.columns)

unique_in_availability = listings.has_availability.unique()

print(unique_in_availability)

listings = listings.drop(['has_availability'], axis=1)
print("Shape after dropping column.{val}".format(val=listings.shape))


# In[16]:

unique_in_license = listings.license.unique()
unique_in_jurisdiction = listings.jurisdiction_names.unique()

print(unique_in_license)
print(unique_in_jurisdiction)
listings = listings.drop(['license','jurisdiction_names'], axis=1)
print("Shape after dropping column.{val}".format(val=listings.shape))


# In[18]:

unique_in_experience = listings.experiences_offered.unique()
print(unique_in_experience)

listings = listings.drop(['experiences_offered'], axis=1)

print("Shape after dropping column.{val}".format(val=listings.shape))


# In[21]:

unique_in_scrape_id = listings.scrape_id.unique()
print(unique_in_scrape_id)

listings = listings.drop(['scrape_id'], axis=1)

print("Shape after dropping column.{val}".format(val=listings.shape))


# In[ ]:

#Filling the missing values appropriately


# In[27]:

mean_ratings = np.mean(listings['review_scores_rating'])

print(mean_ratings)

listings['review_scores_rating'] = listings.review_scores_rating.fillna(mean_ratings)

#print(listings['review_scores_rating'])


# 

# In[20]:

#replacing neighbourhood from 'listings' dataframe to correct value from 'neighbourhood' dataframe

#listings.host_neighbourhood = listings.host_neighbourhood.astype(str)

neighbourhood.neighbourhood = neighbourhood.neighbourhood.astype(str)
listings.host_neighbourhood = listings.host_neighbourhood.fillna("Not Specified")
listings.neighborhood_overview = listings.neighborhood_overview.astype(str)
        
print(listings.host_neighbourhood)


# # Fetching Foursquare's Data

# In[36]:

from __future__ import unicode_literals
import requests
import argparse
import json
import os
from time import gmtime, strftime
import time
import os


searchUrl = 'https://api.foursquare.com/v2/venues/search?ll=42.36,-71.05&oauth_token=SC2QEAC2DQE3C35WMZCCUGM5JUMEMS2MJJOVL4GLO2HPQQKY&v=20161209&limit=50'

r = requests.get(searchUrl, stream = True)

data = dict(r.json())

fname = 'foursquare.json'

rec = dict(r.json())
json.dumps(rec)

with open(fname ,'w')as f:
    json.dump(rec, f)

print("Successfully dumped data to json file.")


# 

# # Fetching Twitter's Data

# In[25]:

API_KEY = 'slbBbLG1sh2hMg1MuIhk8fzNB'
API_SECRET = 'Cl59tZu1Rww9MB6lxq5qxyX6wFAm72DBEIsbVNZPWwzQnhwLat'
ACCESS_TOKEN = '4786768341-9KkLc5dn7qhIn220YeffLyLQJQlDr8EceB3Y7B0'
ACCESS_TOKEN_SECRET = 'ko0ELXDAJ1WJro6foeU7T5gjxE4c8340eeKjquXssVtFq'

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#requests.get(url, auth=auth)


geoloc = "42.36,-71.05,20mi"
searchUrl = "https://api.twitter.com/1.1/search/tweets.json?q=airbnb%20-from%3Astylishrentals&src=typd&lang=en&result_type=mix&count=1500&geocode="+geoloc;

tweets = requests.get(searchUrl, auth=auth, stream = True)

#print(type(r))
#for tweet in r.json():
    # print (tweet)
                
file_name = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
file_name = "data/twitter/"+file_name+".json"

record = dict(tweets.json())
json.dumps(record)
with open(file_name ,'w')as f:
    json.dump(record, f)
twitter_filedata = json.load(open(file_name))
print(twitter_filedata)


# ### Leveraging twitter's pagination to get value from next 10 pages

# In[26]:

max_count = 100
counter = 1


# In[28]:

def getNextResults(twitter_filedata):
    return twitter_filedata['search_metadata']['next_results']


# In[33]:

for i in range(1,3):
    toAppend = getNextResults(twitter_filedata)
    newURL = "https://api.twitter.com/1.1/search/tweets.json"+toAppend

    tweets = requests.get(searchUrl, auth=auth, stream = True)
    file_name = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    file_name = "data/twitter/"+file_name+".json"

    record = dict(tweets.json())
    json.dumps(record)
    with open(file_name ,'w')as f:
        json.dump(record, f)
    twitter_filedata = json.load(open(file_name))
    
    time.sleep(3)


# 

# In[ ]:



