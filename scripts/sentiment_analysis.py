#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import nltk
from pandas.core.common import flatten
import math
import re
from collections import Counter
import operator
import os
import numpy as np
import matplotlib.pyplot as plt
from ttp import ttp
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import re


nltk.download('stopwords')
nltk.download('punkt')
data = pd.read_json('candidatedb.json') 
additional  = ['rt','rts','retweet']
swords = set(nltk.corpus.stopwords.words('polish'))
data.drop_duplicates(subset='full_text',inplace=True)

# In[178]:


def validate(string):
    return re.sub(":\w+","", string)


# In[179]:


data['processed_text'] = data['full_text'].str.lower()            .str.replace('@\w+','')            .str.replace('#\w+','')            .str.replace('(http|https):\/\/\w+.+[^ alt]', '')            .str.replace('[,-:()-]',' ')            .apply(lambda x: [i for i in x.split() if i.isalpha() and len(i)>1])            .apply(lambda x: [i for i in x if not i in swords])


# In[180]:


morf = morfeusz2.Morfeusz()


# In[181]:


def lemm(f):
    try:
        analysis=morf.analyse(f)
        return analysis[0][2][1]
    except:
        return ''


# In[182]:


data['processed_text']=data['processed_text'].apply(lambda x: [lemm(i) for i in x])
data['processed_text']=data['processed_text'].apply(lambda x: [validate(i) for i in x])


# In[183]:



# In[184]:


p = ttp.Parser()
data['tags']=data['full_text'].apply(lambda x: p.parse(x).tags)


# In[185]:


DUDA = "Duda"
KIDAWA = "Kidawa"
KOSINIAK = "Kosiniak"
BIEDRON = "Biedron"
BOSAK = "Bosak"
HOLOWNIA = "Holownia"

CANDIDATES = [DUDA, KIDAWA, KOSINIAK, BIEDRON, BOSAK, HOLOWNIA]

DUDA_ACCOUNTS = ['AndrzejDuda', 'AndrzejDuda2020', 'mecenasJTK', 'jbrudzinski', 'AdamBielan', 'pisorgpl']
KIDAWA_ACCOUNTS = ['M_K_Blonska', 'adamSzlapka', 'Arlukowicz', 'Platforma_org']
BIEDRON_ACCOUNTS = ['RobertBiedron', 'poselTTrela', 'B_Maciejewska', '__Lewica']
KOSINIAK_ACCOUNTS = ['KosiniakKamysz', 'magdasobkowiak', 'DariuszKlimczak', 'nowePSL']
BOSAK_ACCOUNTS = ['krzysztofbosak', 'Bosak2020', 'PUsiadek', 'annabrylka', 'Konfederacja_']
HOLOWNIA_ACCOUNTS = ['szymon_holownia', 'michalkobosko']

def add_candidate(name):
    if name in DUDA_ACCOUNTS:
        return DUDA
    if name in KIDAWA_ACCOUNTS:
        return KIDAWA
    if name in BIEDRON_ACCOUNTS:
        return BIEDRON
    if name in KOSINIAK_ACCOUNTS:
        return KOSINIAK
    if name in BOSAK_ACCOUNTS:
        return BOSAK
    if name in HOLOWNIA_ACCOUNTS:
        return HOLOWNIA
    else: 
        return "undefined"


# In[186]:



data['candidate']=data['user'].apply(lambda x: add_candidate(x.get('screen_name')))
data['user_name']=data['user'].apply(lambda x: x.get('screen_name'))

candidate_dataframes=[]
duda_data=data.loc[data['candidate'] == DUDA]
candidate_dataframes.append((duda_data,DUDA))
kidawa_data=data.loc[data['candidate'] == KIDAWA]
candidate_dataframes.append((kidawa_data,KIDAWA))
bosak_data=data.loc[data['candidate'] == BOSAK]
candidate_dataframes.append((bosak_data,BOSAK))
kosiniak_data=data.loc[data['candidate'] == KOSINIAK]
candidate_dataframes.append((kosiniak_data,KOSINIAK))
biedron_data=data.loc[data['candidate'] == BIEDRON]
candidate_dataframes.append((biedron_data,BIEDRON))
holownia_data=data.loc[data['candidate'] == HOLOWNIA]
candidate_dataframes.append((holownia_data,HOLOWNIA))


# In[197]:


def create_word_cloud(data,column,name):
    bigstring = data[column].apply(lambda x: ' '.join(x)).str.cat(sep=' ')
    plt.figure(figsize=(12,12))
    wordcloud = WordCloud(stopwords=STOPWORDS,
                              background_color='white',
                              collocations=False,
                              width=1200,
                              height=1000
                             ).generate(bigstring)
    plt.axis('off')
    wordcloud.to_file("../clouds/{}".format(name))


# In[198]:


def plot_chart(data,column,name):
    p=[]
    bigstring = data[column].apply(lambda x: p.append(x))
    p=list(flatten(p))

    labels, values = zip(*Counter(p).most_common(10))

    plt.figure(figsize=(20,12))
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width*0.7,color = ['red', 'green','blue','orange'])
    plt.xticks(indexes + width*0.1, labels)
    plt.savefig("../charts/{}".format(name))
    plt.close()


# In[199]:


def reply(data,count,name):
    sp=[]
    k=data['in_reply_to_screen_name'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    res=[]
    sp=Counter(sp).most_common(count)
    for val in sp: 
        if val[0] is not  None : 
            res.append(val)
            
    labels, values = zip(*res)

    plt.figure(figsize=(30,12))
    indexes = np.arange(len(labels))
    width = 0.7

    plt.bar(indexes, values, width, color = ['red', 'green','blue','orange'])
    plt.xticks(indexes + width*0.1, labels)
    plt.savefig("../charts/{}".format(name+"_replies.png"))
    plt.close()


# In[200]:

cloudsdir = '../clouds'
chartsdir = '../charts'
tabledir = '../tables'

try:
    os.mkdir(cloudsdir)
    os.mkdir(chartsdir)
    os.mkdir(tabledir)
except FileExistsError:
    print("")


# In[201]:


for c in candidate_dataframes:
    create_word_cloud(c[0],'processed_text',str(c[1])+'_common_words'+".png")
    plot_chart(c[0],'processed_text',str(c[1])+'_common_words'+".png")
    plot_chart(c[0],'tags',str(c[1])+'_tags'+".png")
    create_word_cloud(c[0],'tags',str(c[1])+"_tags.png")
    reply(c[0],10,str(c[1]))
    
create_word_cloud(data,'processed_text','all_common_words'+".png")
create_word_cloud(data,'tags','all_common_tags'+".png")
plot_chart(data,'processed_text','all_common_words'+".png")
plot_chart(data,'tags','all_common_tags'+".png")
reply(data,10,"all")


# In[202]:


def most_common(data,column,quantity):
    sp = []
    k = data[column].apply(lambda x: sp.append(x))
    sp = list(flatten(sp))
    c = Counter(sp).most_common(quantity)
    c = list(filter(lambda x: str(type(x[0]))!="<class 'NoneType'>", c))
    return c
    
def pd_to_html(p,name,column):
    pd.set_option('colheader_justify', 'center')
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title><meta charset="UTF-8"></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''
    with open('../tables/{}.html'.format(name+"_"+column), 'w', encoding="utf-8") as f:
        f.write(html_string.format(table=p.to_html(classes='mystyle')))


# In[208]:


for c in candidate_dataframes:
    p=pd.DataFrame(most_common(c[0],"processed_text",12), columns =['słowo',  'ilość'])
    pd_to_html(p,str(c[1]),"common_words")
    p=pd.DataFrame(most_common(c[0],"tags",12), columns =['tag',  'ilość'])
    pd_to_html(p,str(c[1]),"tags")    
    p=pd.DataFrame(most_common(c[0],"in_reply_to_screen_name",12), columns =['użytkownik',  'ilość'])
    pd_to_html(p,str(c[1]),"replies")

p=pd.DataFrame(most_common(data,"processed_text",15), columns =['word',  'ilość'])
pd_to_html(p,"all","common_words")
p=pd.DataFrame(most_common(data,"tags",15), columns =['tag',  'ilość'])
pd_to_html(p,"all","tags")
p=pd.DataFrame(most_common(c[0],"in_reply_to_screen_name",12), columns =['użytkownik',  'ilość'])
pd_to_html(p,"all","replies")


# In[204]:


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(data):
    sp=[]
    k=data['processed_text'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    return Counter(sp)


# In[205]:


similarity={}
for i in range(len(candidate_dataframes)):
    c=candidate_dataframes[i]
    similarity[str(c[1])]={}
    for j in range(len(candidate_dataframes)):
        if(i!=j):
            ca=candidate_dataframes[j]
            similarity[str(c[1])][str(ca[1])]=get_cosine(text_to_vector(c[0]), text_to_vector(ca[0]))

for c in similarity.items():
    similarity[str(c[0])]=dict(sorted(c[1].items(), key=operator.itemgetter(1),reverse=True))


# In[209]:


for c in similarity.items():
    p=pd.DataFrame.from_dict(c[1],orient='index').reset_index()
    p.columns = ['Kandydat', 'Podobieństwo']
    pd_to_html(p,str(c[0]),"similarity")


# In[ ]:




