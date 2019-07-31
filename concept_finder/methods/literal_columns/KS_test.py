# Two-sample Kolmogorov-Smirnov Test in Python Scipy

# two arrays of sample observations assumed to be drawn from a continuous distribution, sample sizes can be different

# The Kolmogorov–Smirnov statistic quantifies a distance between the empirical distribution functions of two samples.

from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu
import numpy as np

from collections import OrderedDict

import json
import operator
# data generated from SNORQL queries
train_labels = []
train_data = {}

# data generated from golden data set
test_instances = []
test_data = {}

def test():

    with open('train_data.json') as f:
        train_data = json.load(f)
        train_labels = list(train_data.keys())

    with open('test_data.json') as f:
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
            p = mannwhitneyu(x, y)[1]
            dictionary[train_labels[j]] = p

        sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

        # print (type(sorted_dictionary))

        rank = 0
        for z in range(len(sorted_dictionary)):
            if sorted_dictionary[z][0] == test_data[test_instances[i]]["uri"]:
                rank = (z+1)
        
        print (f'{test_data[test_instances[i]]["uri"]:{60}} {rank:{10}}')
        
        # for z in range(len(sorted_dictionary)):
        #     print(f'{sorted_dictionary[z][0]:{60}} {sorted_dictionary[z][1]:{5}}')

        rank_reciprocal_sum += 1/rank

    print ("test_MRR : ", rank_reciprocal_sum/len(test_data))

def findNearestNeighbours(literalValuesList):

    with open('train_data.json') as f:
        train_data = json.load(f)
        train_labels = list(train_data.keys())

    k = 5
    # dictionalty to put (URI:pValue) pairs
    dictionary = OrderedDict()

    for j in range(len(train_data)):
            train_list = train_data[train_labels[j]]
            p = mannwhitneyu(literalValuesList, train_list)[1]
            dictionary[train_labels[j]] = p

    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    
    knn = []

    for i in range(k):
        knn.append(sorted_dictionary[i][0])

    return knn


# test run to calculate accuracy measures
test()

# caddidate retrival for numerical data column
# print(findNearestNeighbours([122, 135, 140, 127, 123.8, 120, 120.5, 133.5, 111.5]))



























