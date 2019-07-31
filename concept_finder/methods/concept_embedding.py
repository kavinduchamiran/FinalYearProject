"""
first method of the process
try to figure out concept of a column using a trained concept embedding model
we are using 2 CE models, TransE and TransH
"""

from external_libraries.open_ke import models, config

import logging
logging.getLogger('tensorflow').disabled = True

import pickle

# entity to id mappings and concept to id mappings
label_ent = pickle.load(open('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/label_ent.pickle', 'rb'))
label_rel = pickle.load(open('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/label_rel.pickle', 'rb'))
reverse_label_rel = {v: k for k, v in label_rel.items()}

# TransE
con1 = config.Config()
con1.set_in_path('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/')
con1.set_import_files('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/TransE/model.vec.tf')
con1.set_work_threads(16)
con1.set_dimension(200)

con1.init()
con1.set_model(models.TransE)

# TransH
con2 = config.Config()
con2.set_in_path('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/')
con2.set_import_files('../external_libraries/open_ke/benchmarks/DBPEDIA_T2D_BIG/TransH/model.vec.tf')
con2.set_work_threads(16)
con2.set_dimension(200)

con2.init()
con2.set_model(models.TransH)

def predict_concept_transE(e1, e2, k=1):
    e1, e2 = label_ent.get(e1, None), label_ent.get(e2, None)
    if e1 and e2:
        results = []
        predictions = con1.predict_relation(e1, e2, k)
        for pred in predictions:
            results.append(reverse_label_rel[pred])
        return results
    return None


def predict_concept_transH(e1, e2, k=1):
    e1, e2 = label_ent.get(e1, None), label_ent.get(e2, None)
    if e1 and e2:
        results = []
        predictions = con2.predict_relation(e1, e2, k)
        for pred in predictions:
            results.append(reverse_label_rel[pred])
        return results
    return None

# print(predict_concept_transE(1,2,5))