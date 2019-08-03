from SPARQLWrapper import SPARQLWrapper, JSON
from multiprocessing.dummy import Pool as ThreadPool
import os

pool = ThreadPool()

rows = []
triplets = []
labels = {}

"""
This extracts the concepts
"""

# try:
#     os.remove('dbr_dbo_dbr.txt')
# except:
#     pass
try:
    os.remove('dbr_dbo_dbr.txt')
except:
    pass

count = 0
total = 0

def query_dbpedia_concept(subject):
    global count
    count += 1
    print(count / total)
    
    label, uri = subject.split('\t')

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
                SELECT ?p ?o
                WHERE
                {
                <%s> ?p ?o
                }
            """ % uri)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"]):
        triplets = results["results"]["bindings"]

        for triple in triplets:
            predicate = triple['p']['value']
            object = triple['o']['value']

            if 'http://dbpedia.org/ontology' in predicate and 'http://dbpedia.org/ontology/wiki' not in predicate \
                    and 'http://dbpedia.org/resource' in object:
                with open('dbr_dbo_dbr.txt', 'a+', encoding='utf8') as dest:
                    dest.write("{}\t{}\t{}\n".format(uri, predicate, object))

    sparql.setQuery("""
                    SELECT ?s ?p
                    WHERE
                    {
                    ?s ?p <%s>
                    }
                """ % uri)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"]):
        triplets = results["results"]["bindings"]

        for triple in triplets:
            predicate = triple['p']['value']
            subject = triple['s']['value']

            if 'http://dbpedia.org/ontology' in predicate and 'http://dbpedia.org/ontology/wiki' not in predicate \
                    and 'http://dbpedia.org/resource' in subject:
                with open('dbr_dbo_dbr.txt', 'a+', encoding='utf8') as dest:
                    dest.write("{}\t{}\t{}\n".format(subject, predicate, uri))




rows = open('./label_to_uri_cleaned.txt', encoding="utf8").read().split('\n')
rows = list(set(rows))

total = len(rows)

pool.map(query_dbpedia_concept, rows)

pool.close()
pool.join()
