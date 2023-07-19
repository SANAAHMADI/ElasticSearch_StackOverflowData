#!/usr/bin/env python
# coding: utf-8

# In[1]:


from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch("http://localhost:9200")
print(es.ping())


# In[ ]:


# with open('NewData.csv',encoding="utf8") as f:
#     reader = csv.DictReader(f)
#     helpers.bulk(es, reader, index='news')
    
from elasticsearch import helpers, Elasticsearch
import pandas as pd
import json

df = pd.read_csv("NewData.csv",encoding="utf8")
json_str = df.to_json(orient='records')

json_records = json.loads(json_str)

es = Elasticsearch()
index_name = 'news'
doctype = 'census_record'
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index=index_name, ignore=400)
action_list = []
for row in json_records:
    record ={
        '_op_type': 'index',
        '_index': index_name,
        '_type' : doctype,
        '_source': row
    }
    action_list.append(record)
helpers.bulk(es, action_list)


# In[ ]:


word = input("Please Enter a word :")
res = es.search(index="news", body={"query": {"match_phrase": {"Body" : word}}})['hits']['hits']

for item in res:
    strWord = item['_source']['Body']
    print(strWord.find(word))


# In[8]:


import persian
def es_iterate_all_documents(es, index, pagesize=250, **kwargs):
    offset = 0
    while True:
        result = es.search(index=index, **kwargs, body={
            "size": pagesize,
            "from": offset
        })
        hits = result["hits"]["hits"]
        # Stop after no more docs
        if not hits:
            break
        # Yield each entry
        yield from (hit['_source'] for hit in hits)
        # Continue from there
        offset += pagesize
        
for entry in es_iterate_all_documents(es, 'news'):
    numPersian = persian.convert_fa_numbers(entry['Pdate'])
    if(numPersian.find('12') != -1):
        print(entry['News Code'],'-',entry['Pdate'])
    elif(numPersian.find('13') != -1):
        print(entry['News Code'],'-',entry['Pdate'])
    


# In[ ]:




