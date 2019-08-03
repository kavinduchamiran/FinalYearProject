"""
this program extracts all the concepts in the t2d tables (from property files)
then build a dataset with __label__URI ...{synonym} where synonym are synonyms of URI label
"""
import json
import pprint

import urllib3
from SPARQLWrapper import SPARQLWrapper, JSON

from external_libraries.helper_functions import iter_folder
import csv
import re

properties = iter_folder('../../concept_finder/datasets/entity_extractor/property')

con_labels = {}

def query_dbpedia_label(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
                SELECT ?o
                WHERE
                {
                <%s> <http://www.w3.org/2000/01/rdf-schema#label> ?o
                }
            """ % uri)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    labels = []
    if(results['results']['bindings']):
        for object in results['results']['bindings']:
            labels.append(object['o']['value'])
    return labels


def query_datamuse_label(label):
    url = 'https://api.datamuse.com/words?ml=%s' % label.replace(' ', '%20')
    http = urllib3.PoolManager()

    req = http.request('GET', url)
    labels = []
    if req.status == 200:
        json_data = json.loads(req.data)
        for res in json_data:
            labels.append(res['word'])

    return labels


for file in properties:
    path = '../../concept_finder/datasets/entity_extractor/property/' + file
    rows = csv.reader(open(path))

    for a, _, _, _ in rows:
        con_labels[a] = []

for k, _ in con_labels.items():
    # add all labels from dbpedia
    con_labels[k].extend(map(str.lower, query_dbpedia_label(k)))

    # add more synonyms from datamuse
    k_label = k[28:]
    words = re.findall('[a-zA-Z][^A-Z]*', k_label)
    word = "+".join(map(str.lower, words))
    con_labels[k].extend(query_datamuse_label(word)[:20])

# grouping labels that may have same uri
tuples = []
# con_filtered = {}
for uri, values in con_labels.items():
    for value in values:
#         con_filtered[value] = []
        tuples.append((uri, value))
#
# for (k, v) in tuples:
#     con_filtered[v].append(k)
tuples = list(set(tuples))
# con_filtered = {k: list(set(v)) for k, v in con_filtered.items()}

pprint.pprint(tuples)

# write to dataset file
#  __label__URI word

dest = open('./fastText-0.9.1/training_data/train_fasttext2.txt', 'a+', encoding='utf8')
for uri, label in tuples:
    x = '__label__' + uri[28:] + ' '
    dest.write("{}{}\n".format(x.lower(), label.replace(' ', '')))

# head -n 8964 train_fasttext.txt > t2d.train
# tail -n 2242 train_fasttext.txt > t2d.valid

# ./fasttext supervised -input ./training_data/t2d.train -output ./models/t2d -lr 0.5 -epoch 25 -dim 50 -loss one-vs-all