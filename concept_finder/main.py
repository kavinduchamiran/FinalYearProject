"""
the startup point of the project
this file reads a set of tables and output matching concept(s) for each column
and the precision, recall and f1 score

Copyright 2019 Kavindu Chamiran | Amila Rukshan
"""

from file_readers import read_t2d_table, read_t2d_property
from query_dbpedia import query_dbpedia_lookup_endpoint
from methods import concept_embedding, helper_functions
from collections import Counter

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd

search_space = 20

def find_concepts():
    dataset_folder = './datasets/test_files/tables/'
    file_list = helper_functions.iter_folder(dataset_folder, 'json')

    for file in file_list:
        temp_results = {}
        final_results = {}

        has_header, sub_col_idx, columns = read_t2d_table(file + '.json')

        df = pd.DataFrame(columns).transpose()

        print(df.head().to_string())
        print()
        
        property = read_t2d_property(file + '.csv')

        # finding concept of the subject column

        sub_column = columns[sub_col_idx]
        if has_header:
            sub_column = sub_column[1: min(len(sub_column), search_space)]

        sub_results = []

        for e in sub_column:
            result = query_dbpedia_lookup_endpoint(e)
            sub_results.extend(result)

        if not sub_results:
            final_results[sub_col_idx] = None
        else:
            final_results[sub_col_idx] = helper_functions.find_deepest_concept(Counter(sub_results))

        # finding concepts of remaining columns

        for idx, column in enumerate(columns):
            if idx == sub_col_idx:
                continue

            if has_header:
                column = column[1:min(len(column), search_space)]

            temp_results[idx] = []

            for r1, r2 in zip(sub_column, column):
                r1_uri, r2_uri = helper_functions.fuzzy_match(r1.encode('ascii', 'ignore')), \
                                 helper_functions.fuzzy_match(r2.encode('ascii', 'ignore'))

                result = concept_embedding.predict_concept_transE(r1_uri, r2_uri, 1)
                temp_results[idx].append(result)

            final_results[idx] = max(temp_results[idx], key=temp_results[idx].count)

        for c, v in final_results.items():
            print(c, v)

    print()
    print()

find_concepts()

#find . -size +5M | cat >> .gitignore
