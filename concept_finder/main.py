"""
the startup point of the project
this file reads a set of tables and output matching concept(s) for each column
and the precision, recall and f1 score

Copyright 2019 Kavindu Chamiran | Amila Rukshan
"""

from file_readers import read_t2d_table, read_t2d_property
from query_dbpedia import query_dbpedia_lookup_endpoint
from methods import concept_embedding as ce
from methods import find_concept_numerical
from external_libraries.helper_functions import *
from external_libraries.fuzzy import find_concept_fuzzy
from collections import Counter
import pandas as pd
import warnings
import shutil

warnings.simplefilter(action='ignore', category=FutureWarning)

search_space = 10

def find_concepts():
    tp_overall, fp_overall, fn_overall = 0,0,0,
    # tp_overall, fp_overall, fn_overall = 83, 59, 141

    dataset_folder = './datasets/test_files/tables/'
    file_list = iter_folder(dataset_folder, 'json')

    for file in file_list:
        print(file)
        predicted = {}

        has_header, sub_col_idx, columns = read_t2d_table(file + '.json')

        df = pd.DataFrame(columns).transpose()

        print(df.head().to_string())
        print()
        
        actual = read_t2d_property(file + '.csv')

        # ----------------------------------------------------
        # DBPedia lookup endpoint - subject column
        # ----------------------------------------------------

        sub_column = columns[sub_col_idx]
        if has_header:
            # sub_column = sub_column[1:]
            sub_column = sub_column[1: min(len(sub_column), search_space)]

        sub_results = []

        for e in sub_column:
            result = query_dbpedia_lookup_endpoint(e)
            sub_results.extend(result)

        if not sub_results:
            predicted[sub_col_idx] = None
        else:
            predicted[sub_col_idx] = find_deepest_concept(Counter(sub_results))

        # ----------------------------------------------------
        # Concept embedding - TransE - remaining NE columns
        # ----------------------------------------------------

        for idx, column in enumerate(columns):
            temp_results = []

            if idx == sub_col_idx:
                continue

            if is_numerical(column):
                predicted[idx] = None
                continue

            if has_header:
                # column = column[1:]
                column = column[1:min(len(column), search_space)]

            for r1, r2 in zip(sub_column, column):
                r1_uri, r2_uri = fuzzy_match(r1.encode('ascii', 'ignore')), \
                                 fuzzy_match(r2.encode('ascii', 'ignore'))

                result = ce.predict_concept_transE(r1_uri, r2_uri, 1)
                # print(r1, r1_uri, r2, r2_uri, result)
                temp_results.append(result)

            predicted[idx] = max(temp_results, key=temp_results.count)[0]

        # ----------------------------------------------------
        # Text classification - column headers - Fuzzy
        # if numerical or not found using transE
        # ----------------------------------------------------

        for idx, column in enumerate(columns):
            if predicted[idx] is None or predicted[idx] == 'numerical':
                predicted[idx] = find_concept_fuzzy(column[0])[0]

        # # ----------------------------------------------------
        # # Text classification - column values - FastText
        # # ----------------------------------------------------
        #
        # for idx, column in enumerate(columns):
        #     if predicted[idx] is None or predicted[idx] == 'numerical':
        #         predicted[idx] = fs_predict_concept_header(column[1:])
        #
        # # ----------------------------------------------------
        # # Numerical columns - column values - KS Test
        # # ----------------------------------------------------
        #
        # for idx, column in enumerate(columns):
        #     if predicted[idx] is None or predicted[idx] == 'numerical':
        #         predicted[idx] = find_concept_numerical(column[1:])

        for c, v in predicted.items():
            print(c, ': predicted =', v, '| actual =', actual.get(c, None)),
            
        # get tp, fp, fn
        tp, fp, fn = calculate_tp_fp_fn(actual, predicted)
        tp_overall += tp
        fp_overall += fp
        fn_overall += fn

    # print()
    # print()

        print("Precision: %d Recall: %d F1 score: %d" % get_metrics(tp_overall, fp_overall, fn_overall))
        print("tp_overall: %d, fp_overall: %d, fn_overall: %d" % (tp_overall, fp_overall, fn_overall))
        print()
        print()

        source = './datasets/test_files/tables/' + file + '.json'
        dest = './datasets/test_files/tables/done/' + file + '.json'
        shutil.move(source, dest)

find_concepts()

#find . -size +5M | cat >> .gitignore
