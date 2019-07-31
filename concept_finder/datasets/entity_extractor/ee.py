import os
import json
import codecs
from csv import reader
import random
import urllib3
import re

def special_match(strg, search=re.compile(r'[+a-z]').search):
    # regex at least one a-z
    return bool(search(strg)) and len(strg) < 20

from multiprocessing.dummy import Pool as ThreadPool

rows = []
e2c = []

pool = ThreadPool()

count = 0

def query_dbpedia_lookup_endpoint(x):
    try:
        global count
        count += 1
        print(count / c)

        filename, col, entity_label = xgit 

        url = 'http://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString=%s' % entity_label
        http = urllib3.PoolManager()

        req = http.request('GET', url, headers={'Accept': 'application/json'})

        json_data = json.loads(req.data)

        if json_data['results']:
            uri = json_data['results'][0]['uri']
            with open('label_to_uri.txt', 'a+') as dest:
                dest.write("{}\t{}\n".format(entity_label, uri))
        else:
            with open('label_to_uri_failed.txt', 'a+') as dest:
                dest.write("{}\t{}\t{}\n".format(filename, col, entity_label))
    except Exception as e:
        print(e, x, uri)



for filename in os.listdir('./tables'):
    try:
        instance = './instance/' + filename[:-4] + "csv"
        table = './tables/' + filename[:-4] + "json"

        table = json.load(codecs.open(table, 'r', encoding='utf-8', errors='ignore'))
        has_header = table['hasHeader']
        key_column_idx = table['keyColumnIndex'] if table['hasKeyColumn'] else 0    # if key column is available, take it as
                                                                                   # key column idx, else 0 (left most)
        records = table['relation']
        del records[key_column_idx]

        for idx, col in enumerate(records):
            for i in col:
                rows.append((filename, idx, i))
            # rows.extend(map(str.lower, col))

        for line in instance:
            if line == []:
                continue

            uri, _, label, _ = line
            with open('label_dbr.txt', 'a+') as dest:
                dest.write("{}\t{}\n".format(label, uri))

    except Exception as e:
        print(e)
        print(filename)

# rows = list(set(rows))

rows = [row for row in rows if special_match(row[2])]

c = len(rows)

pool.map(query_dbpedia_lookup_endpoint, rows)

pool.close()
pool.join()
