from suffix_tree import SuffixTree

string = 'banana$'
tree = SuffixTree(string)
assert(len(tree.nodes) == 11)
assert(len(tree.edges) == 10)
for i in range(len(string)):
    assert(tree.edges[0, string[i]])
    
string = 'aaaaa$'
tree = SuffixTree(string)
tree.print_()
print len(tree.nodes)
print len(tree.edges)
assert(len(tree.nodes) == 11)
assert(len(tree.edges) == 10)
for i in range(len(string)):
    assert(tree.edges[0, string[i]])
    
string = """We will search this string for a substring using a suffix tree."""
tree = SuffixTree(string)
assert(tree.has_substring('a sub'))
assert(not tree.has_substring('not a sub'))
assert(tree.has_substring('s'))
assert(not tree.has_substring('suffix treee'))