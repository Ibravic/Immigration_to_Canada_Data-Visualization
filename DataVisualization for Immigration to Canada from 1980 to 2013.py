# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:55:18 2020

@author: Ibrahim
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot') # optional: for ggplot-like style

df_can=pd.read_excel('Canada.xlsx',sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

df_can.columns = list(map(str, df_can.columns))

#### 4. Set the country name as index - useful for quickly looking up countries using .loc method.
df_can.set_index('Country', inplace=True)

#Add total column
df_can['Total'] = df_can.sum(axis=1)

# finally, let's create a list of years from 1980 - 2013
years = list(map(str, range(1980, 2014)))


############### Line Plot ###########################

plt.figure(figsize=(15, 10))

df_can.loc['Egypt',years].plot(kind='line')
plt.title("Immigration from Egypt")
plt.ylabel("Number of immigration")
plt.xlabel("Years")
plt.show()


#####################3   Area Plots   #############################################
df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)

# get the top 5 entries
df_top5 = df_can.head()

# transpose the dataframe
df_top5 = df_top5[years].transpose()

df_top5.index = df_top5.index.map(int) # let's change the index values of df_top5 to type integer for plotting

df_top5.plot(kind='area',figsize=(20, 10)), # pass a tuple (x, y) size)

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()

######################### Histogram ####################################
count,bin_edges=np.histogram(df_can['2013'])
df_can['2013'].plot(kind='hist',xticks=bin_edges,figsize=(15,10))
plt.title('Immigration Trend in 2013')
plt.ylabel('Number of Countries')
plt.xlabel('Number of Immigrants')

plt.show()

df_t = df_can.loc[['Egypt', 'Ghana', 'Cameroon'], years].transpose()
# let's get the x-tick values
count, bin_edges = np.histogram(df_t, 15)

# un-stacked histogram
df_t.plot(kind ='hist', 
          figsize=(15, 10),
          bins=15,
          alpha=0.6,
          xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen'],
          stacked=False
         )

plt.title('Histogram of Immigration from Egypt, Ghana, and Cameroon from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()

################################## Bar Chart ##############################

df_egypt = df_can.loc['Egypt',years]
df_egypt.plot(kind='bar', figsize=(15, 10))

plt.xlabel('Year') # add to x-label to the plot
plt.ylabel('Number of immigrants') # add y-label to the plot
plt.title('Egyptian immigrants to Canada from 1980 to 2013') # add title to the plot

plt.show()


df_egypt.sort_values(ascending=False, axis=0, inplace=True)

df_egypt.head().plot(kind='barh', figsize=(15, 10), rot=90) # rotate the xticks(labelled points on x-axis) by 90 degrees

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Egyptian Immigrants to Canada (Top five years)')


plt.show()


############### Pie Chart ###########################
df_continent=df_can.groupby('Continent', axis=0).sum()

df_continent['Total'].plot(kind='pie' , figsize=(15,8))
plt.show()

########### Box Chart ###################################
df_china=df_can.loc[['China'],years].transpose()

df_china.plot(kind='box')
plt.title('Box chart for China')
plt.ylabel('Number of Immigrations')

plt.show()
######################## Scatter chart #################################
# we can use the sum() method to get the total population per year
df_tot = pd.DataFrame(df_can[years].sum(axis=0))

# change the years to type float (useful for regression later on)
df_tot.index = map(float, df_tot.index)

# reset the index to put in back in as a column in the df_tot dataframe
df_tot.reset_index(inplace=True)

# rename columns
df_tot.columns = ['year', 'total']

df_tot.plot(kind='scatter', x='year',y='total',figsize=(20,10),rot=(90))
plt.show()

###################### Bubble Plots #####################################
df_can_t = df_can[years].transpose() # transposed dataframe

# cast the Years (the index) to type int
df_can_t.index = map(int, df_can_t.index)

# let's label the index. This will automatically be the column name when we reset the index
df_can_t.index.name = 'Year'

# reset index to bring the Year in as a column
df_can_t.reset_index(inplace=True)

# normalize Brazil data
norm_brazil = (df_can_t['Brazil'] - df_can_t['Brazil'].min()) / (df_can_t['Brazil'].max() - df_can_t['Brazil'].min())

# normalize Argentina data
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())

# Brazil
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,                  # transparency
                    color='green',
                    s=df_can_t['Brazil'],  # pass in weights 
                    xlim=(1975, 2015)
                   )

# Argentina
ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Argentina',
                    alpha=0.5,
                    color="blue",
                    s=df_can_t['Argentina'],
                    ax = ax0
                   )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from Brazil and Argentina from 1980 - 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')


############################# Word Count #############################
from wordcloud import WordCloud, STOPWORDS
#import txt file
doc = open('f:\Personal\Data Analysis\My Courses\Data Visualization\HR MBA Project the relationship between resilience and HRM(1).txt', 'r').read()

# instantiate a word cloud object
stopwords = set(STOPWORDS)

doc_wc = WordCloud(
    background_color='white',
    max_words=500,
    stopwords=stopwords
)

# generate the word cloud
stopwords.add('resilience') # add the words that not important to stopwords
doc_wc.generate(doc)


# display the word cloud
fig = plt.figure(figsize=(15,15))

#fig.set_figwidth(14) # set width
#fig.set_figheight(18) # set height

# display the cloud
plt.imshow(doc_wc, interpolation='bilinear')
plt.axis('off')
plt.show()


####################### Regression Chart #################################
import seaborn as sns

plt.figure(figsize=(15, 10))

ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})

ax.set(xlabel='Year', ylabel='Total Immigration')
ax.set_title('Total Immigration to Canada from 1980 - 2013')

####################### Folium - World Map ###################################
import folium
# define the world map
world_map = folium.Map(location=[30.033333, 31.233334], zoom_start=8)

# display world map
world_map.save("mymap.html")
