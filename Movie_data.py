# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import os 
import matplotlib.pyplot as plt
df_list=[]
#Creates an empty list, df_list, to which dictionaries will be appended.
#This list of dictionaries will eventually be converted to a pandas DataFrame
folder='rt_html'
for movie_html in os.listdir(folder):
#Loops through each movie's Rotten Tomatoes HTML file in the rt_html folder
    with open(os.path.join(folder,movie_html),encoding='UTF-8') as file:
    #Opens each HTML file and passes it into a file handle called file
        soup=BeautifulSoup(file,'lxml')
        title=soup.find('title').contents[0][:-len(" - Rotten Tomatoes")]
        audience_score=soup.find('div',class_='audience-score meter').find('span').contents[0][:-1]
        #<span class="superPageFontColor" style="vertical-align:top">94%</span> ->94
        num_audience_ratings=soup.find('div',class_='audience-info hidden-xs superPageFontColor')
        num_audience_ratings=num_audience_ratings.find_all('div')[1].contents[2].strip().replace(',','')
        #strip 去掉一串空格
        #['\n', <span class="subtle superPageFontColor">User Ratings:</span>, '\n        103,672']
        df_list.append({'title': title,
                        'audience_score': int(audience_score),
                        'number_of_audience_ratings': int(num_audience_ratings)})
df1 = pd.DataFrame(df_list, columns = ['title', 'audience_score', 'number_of_audience_ratings'])
df2=pd.read_csv('bestofrt.tsv',sep='\t')
df=pd.merge(df1,df2,on=df1['title'])
df.rename(columns={"title_x": "title"},inplace=True)
df.drop(['key_0','title_y'], axis=1,inplace=True)
graph=plt.scatter(df.audience_score,df.critic_score,)