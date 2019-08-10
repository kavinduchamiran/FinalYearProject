import pickle
import json

concept_to_domain = pickle.load(open('./numerical_concept_to_domain_map.pkl', 'rb'))

for k in concept_to_domain.keys():
    print (k, concept_to_domain[k])

f = open('new_test_data.json')
test_data = json.load(f)
test_instances = list(test_data.keys())

count = 0
for i in range(len(test_data)):
    if concept_to_domain[test_data[test_instances[i]]["uri"]] == None:
        count += 1
        # print (test_data[test_instances[i]]["uri"])
        concept_to_domain[test_data[test_instances[i]]["uri"]] = test_data[test_instances[i]]["domain"]

print(count)

for k in concept_to_domain.keys():
    print (k, concept_to_domain[k])


concept_to_domain['http://dbpedia.org/ontology/populationMetro'] = None

# pickle.dump(concept_to_domain, open('./numerical_concept_to_domain_map.pkl', 'wb'))
