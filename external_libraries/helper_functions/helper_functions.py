"""
some helper functions
"""
import math

from fuzzywuzzy import fuzz
import os
import urllib3
from bs4 import BeautifulSoup as bs
from random import sample
import re

regex = re.compile(r'\d+')

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
    lines = [line.rstrip('\n') for line in open('./datasets/dbpedia_mappings/backup/label_to_uri_cleaned.txt', encoding='utf8')]

    curr_uri = ""
    curr_ratio = -1
    for line in lines:
        label = line.split('\t')[0]
        uri = line.split('\t')[1]
        fzz_ratio = fuzz.ratio(entity_label.lower(), label.lower())
        if fzz_ratio > curr_ratio:
            curr_ratio = fzz_ratio
            curr_uri = uri

    return curr_uri if curr_ratio > 80 else None

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


def is_numerical(column):
    s = sample(column, math.ceil(len(column) * 0.3))
    num = []
    for val in s:
        num.append(2 * len(''.join(regex.findall(str(val)))) >= len(val))
    return all(num)


def calculate_tp_fp_fn(actual, predicted):
    tp = 0
    fp = 0
    fn = 0

    for idx, uri in predicted.items():
        true = actual.get(idx, None)
        if true and uri and uri.lower() == true.lower():
            tp += 1
        elif uri and true and uri.lower() != true.lower() or not uri and true:
            fp += 1
        elif uri and not true:
            fn += 1
        else:
            pass

    return tp, fp, fn


def get_metrics(tp, fp, fn):
    if tp == 0 and fp == 0:
        P = 0
    else:
        P = tp / float(tp + fp) * 100

    if tp == 0 and fn == 0:
        R = 0
    else:
        R = tp / float(tp + fn) * 100

    if P == 0 and R == 0:
        F1 = 0
    else:
        F1 = 2 * P * R / (P + R)

    return P, R, F1
