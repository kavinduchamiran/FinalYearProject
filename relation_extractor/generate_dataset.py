import itertools
import os

from SPARQLWrapper import SPARQLWrapper, JSON
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool()

rows = []
triplets = []
labels = {}

"""
This extracts the relations
"""

try:
    os.remove('dataset.txt')
except:
    pass

count = 0
total = 0

def intersection(lst1, lst2):
    return [v for v in lst1 if v in lst2]

def query_dbpedia_relation(entities):
    # global count
    # count += 1
    # print(count / total)

    e1, e2 = entities[0], entities[1]

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
                SELECT DISTINCT ?p
                WHERE
                {
                <%s> ?p ?o
                }
            """ % e1)

    sparql.setReturnFormat(JSON)
    sparql.addDefaultGraph("http://dbpedia.org")

    results = sparql.query().convert()

    if len(results["results"]["bindings"]):
        e1_res = list(set([x['p']['value'] for x in results["results"]["bindings"] if
                           ('property' in x['p']['value'] or 'ontology' in x['p']['value'])]))

    sparql.setQuery("""
                SELECT DISTINCT ?p
                WHERE
                {
                ?s ?p <%s>
                }
            """ % e2)

    results = sparql.query().convert()

    if len(results["results"]["bindings"]):
        e2_res = list(set([x['p']['value'] for x in results["results"]["bindings"] if
                           ('property' in x['p']['value'] or 'ontology' in x['p']['value'])]))

    if e1_res and e2_res:
        for predicate in intersection(e1_res, e2_res):
            if 'wiki' not in predicate:
                with open('dataset.txt', 'a+', encoding='utf8') as dest:
                    dest.write("{}\t{}\t{}\n".format(e1, predicate, e2))

rows = open('../concept_finder/datasets/entity_extractor/label_to_uri_cleaned.txt').read().split('\n')
rows = list(set(rows))

l = [row.split('\t')[1] for row in rows]
l = list(set(l))

coupled = itertools.permutations(l, 2)

pool.map(query_dbpedia_relation, coupled)

pool.close()
pool.join()
