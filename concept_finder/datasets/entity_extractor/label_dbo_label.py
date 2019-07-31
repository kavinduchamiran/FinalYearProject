import os
import json
import codecs
from csv import reader
from SPARQLWrapper import SPARQLWrapper, JSON

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool()

domain = 'All_URI'
rows = []
triplets = []
labels = {}

"""
This extracts the relations
but property files are in dbo's. not dbr's
"""

count = 0
total = 0

def query_dbpedia_concept(subject):
    global count
    count += 1
    print(count / total)
    
    label, uri = subject.split('\t')
    uri = uri[:-2]
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
                with open('dbr_dbo_dbr.txt', 'a+') as dest:
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
                with open('dbr_dbo_dbr.txt', 'a+') as dest:
                    dest.write("{}\t{}\t{}\n".format(subject, predicate, uri))

def query_dbpedia_relation(subject):
    global count
    count += 1
    print(count / total)
    
    label, uri = subject.split('\t')
    uri = uri[:-2]
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

            if 'http://dbpedia.org/property' in predicate and 'http://dbpedia.org/resource' in object:
                with open('dbr_dbp_dbr.txt', 'a+') as dest:
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

            if 'http://dbpedia.org/property' in predicate and 'http://dbpedia.org/resource' in subject:
                with open('dbr_dbp_dbr.txt', 'a+') as dest:
                    dest.write("{}\t{}\t{}\n".format(subject, predicate, uri))


rows = open('./label_dbr.txt').readlines()
rows = list(set(rows))

total = len(rows)

pool.map(query_dbpedia_concept, rows)

count = 0

pool.map(query_dbpedia_relation, rows)

pool.close()
pool.join()