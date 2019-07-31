"""
some helper functions
"""
from fuzzywuzzy import fuzz
import os
import urllib3
from bs4 import BeautifulSoup as bs

def iter_folder(folder_path, extension=None):
    """
    
    :param folder_path: 
    :return: 
    """
    if extension:
        return [filename[:-len(extension)-1] for filename in os.listdir(folder_path) if filename.endswith(".%s" % extension)]
    return [filename for filename in os.listdir(folder_path)]


def fuzzy_match(entity_label):
    """
    find a closest matching dbr:entity for a given entity label
    eg: "sri lanka" -> dbr:Sri_Lanka
    :param entity_label: label of the entity 
    :return: closest dbr uri
    """
    lines = [line.rstrip('\n') for line in open('./datasets/dbpedia_mappings/dbr_label.txt', encoding='utf8')]
    # lines += [line.rstrip('\n') for line in open('label_dbr.txt', encoding='utf8')]

    curr_uri = ""
    curr_ratio = -1
    for line in lines:
        label = line.split('\t')[0]
        uri = line.split('\t')[1]
        fzz_ratio = fuzz.ratio(entity_label.lower(), label.lower())
        if fzz_ratio > curr_ratio:
            curr_ratio = fzz_ratio
            curr_uri = uri

    return curr_uri


def find_deepest_concept(L):
    maxDepth = -float('inf')
    deepestConceptInClassTree = ""
    for c, v in L.items():
        sub = c
        depth = 0
        while (True):
            http = urllib3.PoolManager()
            uri = 'http://dbpedia.org/ontology/' + sub
            req = http.request('GET', uri)
            soup = bs(req.data, "html.parser")
            soup.prettify()
            try:
                sub = soup.find('a', rel='rdfs:subClassOf').text[4:]
                depth += 1
            except:
                break
        L[c] = depth * v
        if L[c] > maxDepth:
            maxDepth = L[c]
            deepestConceptInClassTree = c

    return 'http://dbpedia.org/ontology/' + deepestConceptInClassTree