#!/usr/bin/env python
# coding: utf-8

# In[48]:


from requests_html import HTMLSession
import csv   
import nest_asyncio

nest_asyncio.apply()
session = HTMLSession()
baseURL = 'https://www.asriran.com'
searchURL = baseURL + '/fa/archive?service_id=-1&sec_id=-1&cat_id=-1&rpp=4000&from_date=1401/01/01&to_date=1401/01/28&p=1'


# In[49]:


asession = HTMLSession()
r =  asession.get(searchURL)
resp=r.text
#print(resp)


# In[ ]:


news = r.html.find('.vizhe_title')
# with open('dataset.csv', 'w') as f:
#     writer = csv.writer(f)
with open('dataset.csv', 'w', encoding='utf-8-sig', newline='') as file:
    data=[]
    data.append('NewsCode')
    data.append('PublishDate')
    data.append('Title')
    data.append('NewsPath')
    data.append('SubTitle')
    data.append('Body')
    data.append('Link')
    data.append('TagTitle')
    writer = csv.writer(file)
    writer.writerow(data)

    for item in news:
        
        itemNews = HTMLSession()
        r = session.get(str(item.absolute_links)[2:][:-2])
        respNews = r.text
        strParagraph=''

        data.append(r.html.find('.news_nav.news_id_c')[0].text)
        data.append(r.html.find('div.header_pdate')[0].text)
        data.append(r.html.find('h1.title a[title]')[0].text)
        data.append(r.html.find('div.news_path a')[1].text)
        
        if len(r.html.find('div.subtitle')) != 0:
            data.append(r.html.find('div.subtitle')[0].text)
        else:
            data.append('')
            
        if len(r.html.find('div.body p')) != 0:
            data.append(r.html.find('div.body p')[0].text)
            for par in r.html.find('div.body p'):
                strParagraph += par.text
                data.append(strParagraph)
        else:
            data.append('')
        
        if len(r.html.find('a.link_en')) != 0:
            data.append(r.html.find('a.link_en')[0].text)
        else:
            data.append('')
        
        if len(r.html.find('divtags_title')) != 0:
            data.append(r.html.find('divtags_title'))
        else:
            data.append('')
            
        writer = csv.writer(file)
        writer.writerow(data)


# In[ ]:




