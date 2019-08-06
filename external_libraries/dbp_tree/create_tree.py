from anytree import Node, RenderTree, find_by_attr

f = open('input.txt', 'r')
lines = f.readlines()[1:]
root = Node(lines[0].split(" ")[0])

for line in lines:
    line = line.split(" ")
    Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))

for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
