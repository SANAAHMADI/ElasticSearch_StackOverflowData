#!/usr/bin/env python
# coding: utf-8

# Loading elasticsearch

# In[110]:


from elasticsearch import Elasticsearch
import pandas as pd
import re
import json
import os

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "O+1q7JnmIkx=CGz_wf8m")
)

# print(es.ping())


# In[60]:


# Create index Question file
dir_path = r'C:\\App\\Data\\Question'

files_list=os.listdir(dir_path)
files_list=['C:\\App\\Data\\Question\\'+x for x in files_list]

df_q = pd.concat(map(pd.read_csv, files_list))
df_q = df_q.fillna("")

mapping = {
     "properties": {
            "ID": {"type": "integer"},
            "Body": {"type": "text"},
            "Tags": {"type": "text"}
         }}

es.indices.create(index="question",mappings=mapping)

for i,row in df_q.iterrows():
    doc = {
      "ID" : row['Id'],
      "Body" : row["Body"],
      "Tags" : row["Tags"]
    }
    es.index(index="question",id=row['Id'],document=doc)
    
es.indices.get(index='question')


# In[62]:


# Create index Answer file
dir_path = r'C:\\App\\Data\\Answer'

files_list=os.listdir(dir_path)
files_list=['C:\\App\\Data\\Answer\\'+x for x in files_list]

df_a = pd.concat(map(pd.read_csv, files_list))
df_a = df_a.fillna("")

mapping = {
     "properties": {
            "ID": {"type": "integer"},
            "PostId" : {"type":"integer"},
            "Text": {"type": "text"}
         }}

es.indices.create(index="answer",mappings=mapping)

for i,row in df_a.iterrows():
    doc = {
      "ID" : row['Id'],
      "Text" : row["Text"],
      "PostId" : row["PostId"]
    }
    es.index(index="answer",id=row['Id'],document=doc)
    
es.indices.get(index='answer')


# In[116]:


def search_text(text):
    results = es.search(index='question',query={"match_phrase":{"Body":text}})
    all_hits = results['hits']['hits']
    
    for num, doc in enumerate(all_hits):
        num = doc["_source"]["ID"]
        results2 = es.search(index='answer',query={"match_phrase":{"PostId":num}})
        if results2['hits']['total']['value'] != 0:
            all_hits2 = results2['hits']['hits']
            for num2, doc2 in enumerate(all_hits2):
                str_text = doc2['_source']['Text']
                urls_list = re.findall(r'(https?://[^\s]+)', str_text)
                # Step 2
                if len(urls_list) != 0 :
                    print ("DOC ID:", doc2["_source"]["ID"], "\n", doc2['_source']['Text'], "\n")
                else :
                    print ("DOC ID:", doc2["_source"]["ID"], "\n", doc2['_source']['Text'], "\n")
        


# In[117]:


search_text('Vue.js')

