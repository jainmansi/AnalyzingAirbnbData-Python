
# coding: utf-8

# # Analyzing distribution of listings based on their neighborhood

# In[2]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns


# In[ ]:




# In[15]:

'''ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

ts = ts.cumsum()

df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))'''

listings = pd.read_csv(r'data\boston-airbnb-open-data\listings.csv')

listings['host_neighbourhood'] = listings.host_neighbourhood.ffill()
#df = df.cumsum()

#df=df['host_neighbourhood'].count()

#nhoodDF = df.host_neighbourhood.unique()
#nhoodDF[nhoodDF('host_neighbourhood')]
#print(df.dtype)
#print(df.describe())
#print(df.head(5))
#plt.figure(); 
#df.plot();
#sdf = (ndf['host_neighbourhood'],ndf['host_neighbourhood'].values_count())
newDF = pd.DataFrame()
newDF['host_neighbourhood']=listings['host_neighbourhood']
#ndf.rename('host_neighbourhood')
#sdf
toplot = pd.DataFrame()
#df['e'] = e
toplot['total_hosts'] = newDF['host_neighbourhood'].value_counts()

toplot = toplot[ toplot['total_hosts'] > 5 ]
#s.reset_index(inplace=True)

#s=s.rename(columns = {'index':'host_neighbourhood'})
#s.index.name = None
toplot.sort_index(ascending=False, inplace=True)
toplot
#s
#type(s)
#ndf=ndf.groupby(['host_neighbourhood']).sum()


listings['price'] = listings.price.apply(lambda x: x.replace('$',''))
listings['price'] = listings.price.apply(lambda x: x.replace('.00',''))
listings['price'] = listings.price.apply(lambda x: x.replace(',',''))
print(type(listings.price[0]))
listings.price = listings.price.astype(np.int64)
print(type(listings.price[0]))


# In[16]:

fig = plt.figure(1, figsize=(20,25))
ax = fig.add_subplot(111)

title="Distribution of listings based on neighbourhood in Boston"

transparency = 0.7
customcmap = sns.color_palette("autumn")


#sns.color_palette("Set2", 10)

toplot['total_hosts'].plot(kind='barh', ax=ax, alpha=transparency, legend=False,color=customcmap, 
                      edgecolor='w', xlim=(0,max(s['total_hosts'])), title=title)

ax.grid(False)
ax.set_frame_on(False)

ax.set_title(ax.get_title(), fontsize=26, alpha=transparency, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.04))

ax.xaxis.set_label_position('top')
xlab = 'Total number of listings'
ax.set_xlabel(xlab, fontsize=20, alpha=transparency, ha='left')
ax.xaxis.set_label_coords(0, 1.02)
ax.xaxis.tick_top()

ylab = 'Neighbourhood in Boston'
ax.set_ylabel(ylab, fontsize=20, alpha=transparency)

ax.yaxis.set_ticks_position('none')
ax.xaxis.set_ticks_position('none')


# In[25]:

plt.figure(figsize=(10,10))

cmap = sns.cubehelix_palette(8, start=.5, rot=-.75, as_cmap=True)

sns.heatmap(listings.groupby([
        'host_neighbourhood', 'bedrooms']).price.mean().unstack(),
            annot=True, 
            fmt=".0f",
           cmap=cmap)


# In[ ]:



