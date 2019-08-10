"""
second method of the process
try to figure out concept of a numerical column using a previously annotated dataset
here we use KNN algorithm with KS test as the distance measure.
candidates are eliminated by heuristics of the concept graph 
"""

from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu

import pickle
from collections import OrderedDict
from anytree import Node, RenderTree, find_by_attr
import json
import operator

def findNearestNeighbours(literalValuesList, K):

    with open('../datasets/numerical_data/train_data.json') as f:
        train_data = json.load(f)
        train_labels = list(train_data.keys())

    k = K
    # dictionalty to put (URI:pValue) pairs
    dictionary = OrderedDict()

    for j in range(len(train_data)):
            train_list = train_data[train_labels[j]]
            p = ks_2samp(literalValuesList, train_list)[1]
            dictionary[train_labels[j]] = p

    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    
    knn = []

    for i in range(k):
        knn.append(sorted_dictionary[i][0])

    # print (knn)
    return knn

def findDomains(k_conceptsList):
    concept_to_domain = pickle.load(open('../datasets/numerical_data/numerical_concept_to_domain_map.pkl', 'rb'))
    found_concept_to_domain = { }
    for concept in k_conceptsList:
        # print(concept, concept_to_domain[concept])
        found_concept_to_domain[concept] = concept_to_domain[concept]
    return found_concept_to_domain

"""
input the concept(without http://dbpedia.org/ontology/) of the subject column found on first step and 
the numerical column extracted from the t2d table
"""
def findNumericalConcept(subject_concept, value_set):
    remove = "$,\"[]()? -!abcdefghijklmnopqstuvw"
    normalized_value_set = []
    for txt in value_set[1:]:
        for r in remove:
            txt = txt.replace(r, '')
        if len(txt) > 0:
            normalized_value_set.append(float(txt))
    # finding the domains correspond to concepts
    candidates_to_domain = findDomains(findNearestNeighbours(normalized_value_set, 20))
    
    predicted_concept = None
    b = False
    for candidate in candidates_to_domain.keys():
        if candidates_to_domain[candidate] != None and candidates_to_domain[candidate][28:] == subject_concept:
            b = True
            predicted_concept = candidate[28:]
            break

    # loading the concept tree
    root = None
    f = open('../datasets/numerical_data/dbp_tree_input.txt', 'r')
    lines = f.readlines()[1:]
    root = Node(lines[0].split(" ")[0])
    for line in lines:
        line = line.split(" ")
        Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))

    if not b:
        min_dis = float('inf')
        min_dist_concept = None
        for candidate in candidates_to_domain.keys():
            x = [ancestor.name for ancestor in find_by_attr(root, subject_concept).ancestors]
            x.append(subject_concept)
            x = set(x)
            y = None
            if candidates_to_domain[candidate] != None:
                try:
                    y = [ancestor.name for ancestor in find_by_attr(root, candidates_to_domain[candidate][28:]).ancestors]
                    y.append(candidates_to_domain[candidate][28:])
                    y = set(y)
                    curr_dis = len(list(x.union(y)-x.intersection(y)))
                    if curr_dis < min_dis:
                        min_dis = curr_dis
                        min_dist_concept = candidate
                except:
                    continue
        predicted_concept = min_dist_concept[28:]

    return predicted_concept

