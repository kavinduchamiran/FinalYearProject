from rdflib.graph import Graph

g = Graph()

print("parsing stared...")
g.parse("raw_infobox_properties_en_uris_simple.nt", format="nt")
print("parsing ended...")

print ("number of triplets : ",len(g))

for subj, pred, obj in g:
    print (subj + " "+pred +" "+ obj)


