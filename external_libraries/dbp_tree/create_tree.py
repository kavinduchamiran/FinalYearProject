from anytree import Node, RenderTree, find_by_attr

with open('input.txt', 'r') as f:
    lines = f.readlines()[1:]
    root = Node(lines[0].split(" ")[0])

    for line in lines:
        line = line.split(" ")
        Node("".join(line[1:]).strip(), parent=find_by_attr(root, line[0]))

    for pre, _, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    
    # print(RenderTree(find_by_attr(root, "Game")))
    # print(RenderTree(find_by_attr(root, "WrittenWork")))