from bs4 import BeautifulSoup
import pickle

floatOrIntPropertyConcepts = []
concept_to_domain = {}

with open("./dbpedia.owl") as owl:
    soup = BeautifulSoup(owl, "lxml")

    myRanges = soup.findAll("rdfs:range", {"rdf:resource": [
        "http://www.w3.org/2001/XMLSchema#float", 
        "http://www.w3.org/2001/XMLSchema#integer",
        "http://www.w3.org/2001/XMLSchema#positiveInteger",
        "http://www.w3.org/2001/XMLSchema#integer",
        "http://www.w3.org/2001/XMLSchema#nonNegativeInteger"
    ]})

    for rnge in myRanges: 
        x = rnge.findParent().findChildren('rdfs:domain')
        if len(x) > 0:
            x = x[0]['rdf:resource']
        else:
            x = None
        floatOrIntPropertyConcepts.append((rnge.findParent()['rdf:about'], x))
        floatOrIntPropertyConcepts.append(rnge.findParent()['rdf:about'])
        # concept_to_domain[rnge.findParent()['rdf:about']] = x


# pickle.dump(floatOrIntPropertyConcepts, open('./floatOrIntPropertyConcepts.pkl', 'wb'))

# pickle.dump(concept_to_domain, open('./numerical_concept_to_domain_map.pkl', 'wb'))

# readList = pickle.load(open('./floatOrIntPropertyConcepts.pkl', 'rb'))


for concept in floatOrIntPropertyConcepts:
    print(concept)

print (len(floatOrIntPropertyConcepts))