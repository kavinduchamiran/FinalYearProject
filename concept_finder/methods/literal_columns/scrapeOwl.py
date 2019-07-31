from bs4 import BeautifulSoup
import pickle

floatOrIntPropertyConcepts = []

with open("./dbpedia.owl", encoding="utf8") as owl:
    soup = BeautifulSoup(owl, "lxml")

    myRanges = soup.findAll("rdfs:range", {"rdf:resource": [
        "http://www.w3.org/2001/XMLSchema#float", 
        "http://www.w3.org/2001/XMLSchema#integer",
        "http://www.w3.org/2001/XMLSchema#positiveInteger",
        "http://www.w3.org/2001/XMLSchema#integer" 
    ]})

    for rnge in myRanges: 
        floatOrIntPropertyConcepts.append(rnge.findParent()['rdf:about'])


pickle.dump(floatOrIntPropertyConcepts, open('./floatOrIntPropertyConcepts.pkl', 'wb'))

# readList = pickle.load(open('./floatOrIntPropertyConcepts.pkl', 'rb'))

# for concept in readList:
#     print(concept)