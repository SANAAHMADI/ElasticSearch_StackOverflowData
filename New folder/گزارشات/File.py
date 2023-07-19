from elasticsearch import helpers, Elasticsearch
import csv
import os

es = Elasticsearch("http://localhost:9200")
dir_path = r'C:\\App\\Data\\'

l=os.listdir(dir_path)
li=[x.split('.')[0] for x in l]

for path in li:
    with open( dir_path + path + '.csv') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='path')
    print(path)
