from rdflib.graph import Graph

g = Graph()
g.parse("mappingbased_properties_cleaned_en.nt", format="nt")

print ("number of triplets : ",len(g))

for subj, pred, obj in g:
    print (subj + " "+pred +" "+ obj)


