from suffix_tree import SuffixTree

string = 'banana$'
tree = SuffixTree(string)
tree.print_()
assert(len(tree.nodes) == 11)
assert(len(tree.edges) == 10)
for i in range(len(string)):
    assert(tree.edges[0, string[i]])
    
string = 'aaaaa$'
tree = SuffixTree(string)
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

assert(tree.find_substring('We') == 0)
assert(tree.find_substring('this string') == 15)
assert(tree.find_substring('not this string') == -1)