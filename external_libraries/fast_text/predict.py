# using table headers
import fasttext

def fs_predict_concept_header(txt):
    model = fasttext.load_model("../external_libraries/fast_text/model/t2d_v3.bin")
    print(model.predict(txt.replace(' ', '').lower(), 5))
    # return 'http://dbpedia.org/ontology/' +

def fs_predict_concept_cells(column):
    model = fasttext.load_model("../external_libraries/fast_text/model/model_uri_failed.bin")
    predictions = [model.predict(txt.lower())[0][0][9:] for txt in column]
    return max(predictions, key=predictions.count)


# print(fs_predict_concept_header('country'))
# print(fs_predict_concept_header('percapitaincome'))
# print(fs_predict_concept_header('nintendo'))
# print(predict_concept('Population est.'))
# print(predict_concept('A3'))
# print(predict_concept('address'))
# print(predict_concept('alt (m)'))