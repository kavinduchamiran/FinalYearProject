# from methods import concept_embedding as ce
from methods import find_concept_numerical
from file_readers import read_t2d_table, read_t2d_property
from external_libraries import helper_functions as hf
from external_libraries.fuzzy import find_concept_fuzzy

has_header, sub_col_idx, columns = read_t2d_table('13357355_0_5384862281417742530.json')

sub_column = columns[sub_col_idx]

if has_header:
    sub_column = sub_column[1:]

# sub_results = []
#
# for e in sub_column:
#     result = query_dbpedia_lookup_endpoint(e)
#     sub_results.extend(result)
#
# if not sub_results:
#     predicted[sub_col_idx] = None
# else:
#     predicted[sub_col_idx] = hf.find_deepest_concept(Counter(sub_results))

# finding concepts of remaining columns
#
# temp_results = {}
#
# for idx, column in enumerate(columns):
#     print('------------------------')
#     if idx == sub_col_idx:
#         continue
#
#     if has_header:
#         column_ = column[1:]
#
#     temp_results[idx] = []
#
#     for r1, r2 in zip(sub_column, column):
#         r1_uri, r2_uri = hf.fuzzy_match(r1.encode('ascii', 'ignore')), \
#                          hf.fuzzy_match(r2.encode('ascii', 'ignore'))
#         print(r1, r1_uri, r2, r2_uri)
#         result = ce.predict_concept_transE(r1_uri, r2_uri, 1)
#         print(result)

print(find_concept_fuzzy('directors'))