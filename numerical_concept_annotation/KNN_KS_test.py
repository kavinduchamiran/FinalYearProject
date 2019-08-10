
from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu
import numpy as np
import pickle

from collections import OrderedDict
from anytree import Node, RenderTree, find_by_attr

import json
import operator
# data generated from SNORQL queries
train_labels = []
train_data = {}

# data generated from golden data set
test_instances = []
test_data = {}

def findNearestNeighbours(literalValuesList, K):

    with open('train_data.json') as f:
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
    concept_to_domain = pickle.load(open('./numerical_concept_to_domain_map.pkl', 'rb'))
    found_concept_to_domain = { }
    for concept in k_conceptsList:
        # print(concept, concept_to_domain[concept])
        found_concept_to_domain[concept] = concept_to_domain[concept]
    return found_concept_to_domain

def load_tree():
    root = None
    f = open('dbp_tree_input.txt', 'r')
    lines = f.readlines()[1:]
    root = Node(lines[0].split(" ")[0])
    for line in lines:
        line = line.split(" ")
        Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))
    
    ### print the tree
    # for pre, _, node in RenderTree(root):
    #     print("%s%s" % (pre, node.name))
    
    return root


def test():

    with open('train_data.json') as f:
        train_data = json.load(f)
        train_labels = list(train_data.keys())

    with open('new_test_data.json') as f:
        test_data = json.load(f)
        test_instances = list(test_data.keys())
        

    # print(len(train_data))
    # print(len(test_data))

    rank_reciprocal_sum = 0

    for i in range(len(test_data)):
        
        dictionary = OrderedDict()

        x =  test_data[test_instances[i]]["literals"]
        for j in range(len(train_data)):
            y = train_data[train_labels[j]]
            p = ks_2samp(x, y)[1]
            dictionary[train_labels[j]] = p

        sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

        # print (type(sorted_dictionary))

        rank = 0
        for z in range(len(sorted_dictionary)):
            if sorted_dictionary[z][0] == test_data[test_instances[i]]["uri"]:
                rank = (z+1)
        
        print (i, test_data[test_instances[i]]["uri"], rank)
        
        # for z in range(len(sorted_dictionary)):
        #     print(f'{sorted_dictionary[z][0]:{60}} {sorted_dictionary[z][1]:{5}}')

        rank_reciprocal_sum += 1/float(rank)

    print ("test_MRR : ", rank_reciprocal_sum/len(test_data))
    
    true = 0
    root = load_tree()
    for i in range(len(test_data)):
        candidates_to_domain = findDomains(findNearestNeighbours(test_data[test_instances[i]]["literals"], 20))
        
        domain = test_data[test_instances[i]]["domain"][28:]
        uri =  test_data[test_instances[i]]["uri"][28:]
        # tree_node = find_by_attr(root, "Country")
        # print (domain)
        b = False
        for candidate in candidates_to_domain.keys():
            if candidates_to_domain[candidate] != None and candidates_to_domain[candidate][28:] == domain:
                b = True
                if candidate[28:] == uri:
                    true += 1
                else:
                    print(i, "------------------", candidate[28:], uri)
                break
                # return candidate

        if not b:
            min_dis = float('inf')
            min_dist_concept = None
            for candidate in candidates_to_domain.keys():
                x = [ancestor.name for ancestor in find_by_attr(root, domain).ancestors]
                x.append(domain)
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
            # print (i, x,y)
            if min_dist_concept[28:] == uri:
                true += 1
            else:
                print(i, "++++++++++++++++++", min_dist_concept[28:], uri)
            # print (i, min_dist_concept, domain)
        

        # print(i, uri, domain, b)
    print ("accuracy: ", float(true)/len(test_data))
    print ("tp: ", true)
    print ("fp: ", len(test_data) - true)


def findNumericalConcept(subject_concept, value_set):
    remove = "$,\"[]()? -!abcdefghijklmnopqstuvw"
    normalized_value_set = []
    for txt in value_set[1:]:
        for r in remove:
            txt = txt.replace(r, '')
        if len(txt) > 0:
            normalized_value_set.append(float(txt))
    # findign the domains correspond to concepts
    candidates_to_domain = findDomains(findNearestNeighbours(normalized_value_set, 20))
    
    predicted_concept = None
    b = False
    for candidate in candidates_to_domain.keys():
        if candidates_to_domain[candidate] != None and candidates_to_domain[candidate][28:] == subject_concept:
            b = True
            predicted_concept = candidate[28:]
            break

    # loading the concept tree
    root = load_tree()
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


# test run to calculate accuracy measures
test()

con = findNumericalConcept('Hospital', ["Staffed Beds",
"0",
"0",
"407",
"514",
"658",
"146",
"815",
"54",
"0",
"72",
"56",
"323",
"0",
"391",
"112",
"401",
"383",
"369",
"345",
"244",
"640",
"150",
"291",
"198",
"226",
"208",
"198",
"155",
"240",
"302",
"245",
"200",
"465",
"49",
"281",
"168",
"48",
"0",
"92",
"110",
"100",
"238",
"316",
"0",
"0",
"109",
"0",
"156",
"0",
"139",
"99",
"159",
"0",
"0",
"0",
"396",
"2,067",
"0",
"475",
"204",
"154",
"58",
"257",
"333",
"67",
"176",
"349",
"206",
"171",
"50",
"0",
"194",
"168",
"362",
"126",
"666",
"571",
"142",
"180",
"335",
"88",
"1,724",
"0",
"0",
"0",
"55",
"448",
"163",
"412",
"60",
"67",
"0",
"131",
"851",
"70",
"120",
"380",
"130",
"341",
"931",
"309",
"88",
"152",
"0",
"0",
"0",
"319",
"0",
"344",
"214",
"0",
"307",
"124",
"550",
"0",
"415",
"178",
"180",
"301",
"304",
"993",
"0",
"343",
"146",
"494",
"0",
"666",
"226",
"668",
"399",
"0",
"0",
"681",
"0",
"343",
"325",
"110",
"778",
"434",
"227",
"215",
"224",
"270",
"255",
"1,401",
"235",
"0",
"199",
"247",
"360",
"307",
"175",
"210",
"120",
"189",
"0",
"201",
"264",
"99",
"100",
"0",
"268",
"466",
"55",
"19",
"280",
"84",
"881",
"0",
"0",
"229",
"463",
"219",
"518",
"313",
"129",
"786",
"117",
"128",
"870",
"607",
"99",
"112",
"147",
"104",
"444",
"0",
"0",
"177",
"40",
"603",
"915",
"192",
"201",
"20",
"57",
"317",
"506",
"312",
"0",
"158",
"195",
"531",
"0",
"0",
"0",
"197",
"224",
"527",
"0",
"115",
"291",
"53,155"])
print(con)