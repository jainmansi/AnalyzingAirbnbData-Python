
# coding: utf-8

# # Analysis of all the customer reviews over time & over social media

# In[41]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
import datetime
from textblob import TextBlob
import glob
import json
import time
import calendar


# In[2]:

reviews = pd.read_csv(r'data\boston-airbnb-open-data\reviews.csv')

print(reviews.head())


# In[12]:

#print(type(reviews.date[0]))
#df = reviews.head()
#df['year'] = df.date.apply(lambda x: x.split('-')[0])
#type(df.year[0])


# In[3]:

review_count_dates = pd.to_datetime(reviews['date']).value_counts().resample('D').mean().fillna(0)


# In[4]:

fig = plt.figure(1, figsize=(8,8))
ax = fig.add_subplot(111)
ax.grid(False)
ax.set_axis_bgcolor('#FEFDFB')
title='Distribution of reviews over time'
transparency = 0.5
review_count_dates.rolling(window=15).mean().plot(ax=ax, color='#FE8A71', title = title)

ax.set_title(ax.get_title(), fontsize=26, ha='left')
ax.title.set_position((0.1,1.04))

xlab = 'Year'
ax.set_xlabel(xlab, fontsize=15, ha='left')

ylab = 'Number of reviews posted'
ax.set_ylabel(ylab, fontsize=15, ha='left')


# # Analyzing sentiments for Airbnb on Twitter over time

# In[5]:

twitter_sentiment = pd.DataFrame()
twitter_sentiment['year'] = reviews['date']

twitter_sentiment['year'] = twitter_sentiment.year.apply(lambda x: x.split('-')[0])

yearSeq = twitter_sentiment.year.unique()
years = [int(i) for i in yearSeq]
years.sort()
print(years)


# In[6]:

def convert_to_epoc():
    t = calendar.timegm(time.strptime('Jan 01, 2008 @ 00:00:00 UTC',"%b %d, %Y @ %H:%M:%S %Z"))
    return t;


# In[17]:

count = 0
positive = 0
negative = 0
neutral = 0

for filename in glob.glob(r"data\twitter\*.json"):
    with open(filename, 'r') as f:
        twitter_file_data = json.load(f)
        
        for items in twitter_file_data["statuses"]:
    
            blob = TextBlob(items["text"])
            #print(items["text"])
    
            count += 1
            total = 0
    
            for sentence in blob.sentences:
                blob.tags
                blob.noun_phrases
                value = sentence.sentiment.polarity
                #print(value)
                total += value
    
            if(total > 0):
                positive = positive + 1 
            elif total < 0:
                negative +=1
            else:
                neutral +=1
                
print(positive)
print(negative)
print(neutral)


# In[18]:

count


# In[55]:

label_li = ['positive','negative','neutral']
value_li = [positive, negative, neutral]

customer_sentiments = pd.DataFrame(value_li, index=label_li, columns=['twitter_count'])

customer_sentiments['twitter_count']


# In[10]:

airbnb_pos = 0
airbnb_neg = 0
airbnb_neu = 0

reviewDF = pd.DataFrame()
reviewDF['reviews'] = reviews.comments

#print(type(reviewDF.reviews[0]))
reviewDF['reviews'] = reviewDF.reviews.fillna('')
for customer_review in reviewDF.reviews:
    
    blob = TextBlob(customer_review)
    polarity = 0
    
    for sentence in blob.sentences:
        blob.tags
        blob.noun_phrases
        value = sentence.sentiment.polarity
        #print(value)
        polarity += value
    
        if(polarity > 0):
            airbnb_pos += 1 
        elif polarity < 0:
            airbnb_neg +=1
        else:
            airbnb_neu +=1
                
print(airbnb_pos)
print(airbnb_neg)
print(airbnb_neu)


# In[56]:

airbnb_sentiments_li = [airbnb_pos,airbnb_neg,airbnb_neu]

customer_sentiments['airbnb_count'] = airbnb_sentiments_li
customer_sentiments


# In[23]:

airbnb_row = reviews.shape[0]
airbnb_row


# In[57]:

#converting values to percentage

customer_sentiments.twitter_count = customer_sentiments.twitter_count.apply(lambda x: x*100/count)
customer_sentiments.airbnb_count = customer_sentiments.airbnb_count.apply(lambda x: x*100/airbnb_row)


# In[118]:

customer_sentiments['polarity'] = customer_sentiments.index
customer_sentiments.reset_index


# In[117]:




# In[136]:

li_twi = customer_sentiments.twitter_count
li_abnb = customer_sentiments.airbnb_count


toplot = pd.DataFrame()
toplot['Twitter'] = li_twi
toplot['Airbnb'] = li_abnb
newplot = toplot.T
newplot


# In[140]:

barfig = plt.figure(1, figsize=(8,8))
ax = barfig.add_subplot(111)
ax.grid(False)

colors = ['#ED5784','#FFD91E','#AA61CE']

my_plot = newplot.plot(kind='bar',
                       stacked=True,
                       title="Sentimental analysis across airbnb and twitter",
                       ax=ax,
                       color=colors,
                       alpha=0.75)

ax.set_xticklabels(newplot.index,
                   rotation=30, 
                   fontsize=14, 
                   alpha=0.75)

ax.set_title('Sentimental analysis across airbnb and twitter', 
             fontsize=20, 
             alpha=0.90)

my_plot.set_xlabel("Platforms")
my_plot.set_ylabel("Percentage")

