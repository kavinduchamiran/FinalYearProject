from anytree import Node, RenderTree, find_by_attr

<<<<<<< HEAD
f = open('input.txt', 'r')
lines = f.readlines()[1:]
root = Node(lines[0].split(" ")[0])

for line in lines:
    line = line.split(" ")
    Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))

for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
=======
""" 
load the tree from (class, sub-class) pair relatioships defined in the input.txt
"""
def load_tree():
    root = None
    f = open('input.txt', 'r')
    lines = f.readlines()[1:]
    root = Node(lines[0].split(" ")[0])
    for line in lines:
        line = line.split(" ")
        Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))
    return root
    
""" 
return the concept that is deepest and with most number of occurences
"""
def find_deepest_concept(L):
    maxDepth = -float('inf')
    deepestConceptInClassTree = ""
    root = load_tree()
    for c, v in L.items():
        depth = find_by_attr(root, "Guitarist").depth
        L[c] = depth * v
        if L[c] > maxDepth:
            maxDepth = L[c]
            deepestConceptInClassTree = c

    return 'http://dbpedia.org/ontology/' + deepestConceptInClassTree


# x = find_by_attr(root, "Guitarist")
# print(x.depth)

### for print the tree
# for pre, _, node in RenderTree(root):
#     print("%s%s" % (pre, node.name))
>>>>>>> 316850f924aa69913f5a05a3271a86a03df65455
