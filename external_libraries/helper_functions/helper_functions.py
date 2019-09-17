"""
some helper functions
"""
import math
import re

from fuzzywuzzy import fuzz
import os
import urllib3
from bs4 import BeautifulSoup as bs
from random import sample

# regexes = [
#     '(\\d+)' + '(,)' + '(\\d+)',    # 123,456
#     '(\\d+)' + '(.)' + '(\\d+)',    # 123.456
#     '\\d+',    # 123
#     '\\d+',    # 123
#
# ]

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


def is_numerical_column(column):
    """
    given a column, sample 30% of it
    for each value, check [0-9] count > [a-zA-Z] count
    return true if ^ true for all in sample
    :param column: a column: list from a table
    :return: True if all cells in sampled list are numerical
    """
    numerical = []
    size = math.ceil(len(column)*0.3)
    col_sample = sample(column, size)
    regex = re.compile(r'\d')
    for val in col_sample:
        num_count = len(''.join(regex.findall(str(val))))
        numerical.append(2 * num_count >= len(str(val)))
    return all(numerical)




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


def calculate_tp_fp_fn(actual, predicted):
    tp = 0
    fp = 0
    fn = 0

    for idx, uri in predicted.items():
        # if uri is not defined in property files, its not added to actual dict. so no need to continue.
        # if uri is None:
        #     continue

        true = actual.get(idx, None)
        pred = uri
        print(true, "-------", pred)

        if true == pred:
            tp += 1
        else:
            if true is not None:
                fn += 1
            else:
                fp += 1

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


is_numerical_column([1, 2, 3, 4])
is_numerical_column(['1980-19-10', '1221-21-32'])
is_numerical_column(['(707) 785-3415', '(707) 385-3415'])
is_numerical_column(['613m', '62113m'])
is_numerical_column(['$1,800', '&1,800'])
is_numerical_column(['Promoted Sept 2007', 'Promoted Oct 2007'])
is_numerical_column(['52', '244'])
is_numerical_column(['colombo 1', 'united 40'])
