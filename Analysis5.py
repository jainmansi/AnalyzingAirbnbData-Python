
# coding: utf-8

# # Airbnb listing's performance over price.

# In[2]:

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')


# In[14]:

calendar = pd.read_csv(r'data\boston-airbnb-open-data\calendar.csv')

print(calendar.head())

#calendar['listing_date'] =  pd.to_datetime(calendar['date'], format="%Y/%m/%d")
#print(type(calendar.listing_date[0]))

listings = pd.read_csv(r'data\boston-airbnb-open-data\listings.csv')

calendar.set_index(['listing_id'],inplace=True)
calendar.head()

reviews = pd.read_csv(r'data\boston-airbnb-open-data\reviews.csv')
reviews.set_index(['listing_id'],inplace=True)
print(reviews.head())


# In[5]:

new_calDF = calendar.dropna()

new_calDF.loc[:,'date'] = pd.to_datetime(new_calDF['date'])


def fun(rows):
    return float(rows['price'].split('$')[1].replace(',',''))
new_calDF.loc[:,'price'] = new_calDF.apply(fun,axis=1)
new_calDF.head()


# In[9]:

review_num = pd.DataFrame(reviews.groupby(level=0).agg(len)['id'])

review_num.columns = ['number']

price_id = pd.DataFrame(new_calDF.groupby(level=0).agg(np.mean))

price_rev = pd.merge(review_num,price_id,
                    how='inner',
                    left_index=True,
                    right_index=True)

price_rev.sort_values(by='price',
                      inplace=True)


# In[11]:

fig = plt.figure(1, figsize=(10,10))
ax = fig.add_subplot(111)

plt.scatter(data=price_rev,
            x='price',
            y='number', 
            color = '#CD6B97')

ax.set_xlabel('Price of listing (in $)',
             fontsize=25, 
            alpha=0.5)

ax.set_ylabel('Count of posted reviews',
             fontsize=25, 
              alpha=0.5)

ax.set_title('Reviews vs. Price', 
             fontsize=30, 
             alpha=0.65)

plt.xlim(0,1400)
plt.ylim(0,450)


# In[30]:

toplot_listings = listings[['host_since','bedrooms']]

toplot_listings.dropna(inplace=True)

toplot_listings[ toplot_listings['bedrooms'] == 0 ]=1 # considering 0 bedrooms as 1 bedroom.

toplot_listings['price']=listings.apply(lambda x: float(x['price'].split('$')[1].replace(',','')),axis=1)

toplot_listings['price_per_bedroom'] = toplot_listings['price']/toplot_listings['bedrooms']

toplot_listings['host_since'] = pd.to_datetime(toplot_listings['host_since'])
toplot_listings.set_index(['host_since'],inplace=True)

toplot_listings = toplot_listings[toplot_listings.index>='2008'] #since airbnb was funded in 2008


plt.figure(figsize = (10,10))
sns.barplot(x = toplot_listings.index.strftime('%Y'),
            y = toplot_listings['price_per_bedroom'],
           palette  = sns.color_palette("GnBu_d"))

plt.xticks(rotation=90)
           
plt.xlabel('Year the host joined Airbnb')
plt.ylabel('Price per bedroom in $')


# Pricing is available only when the listing is available

# In[ ]:



