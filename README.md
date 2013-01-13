Suffix Trees in Python
================================

Based off of Mark Nelson's C++ implementation of Ukkonen's algorithm. Ukkonen's
algorithm gives a O(n) + O(k) contruction time for a suffix tree, where n is 
the length of the string and k is the size of the alphabet of that string. 
Ukkonen's is an online algorithm, processing the input sequentially and producing 
a valid suffix tree at each character.

How to use
----------

	string = "I need to be searched!"
    tree = SuffixTree(string)
	index_of_need = tree.find_substring("need")

Usage note
----------

This library is mostly an academic exercise. 
If you need an efficient library
I would recommend a python-wrapped c implementation, 
such as [this one](http://www.daimi.au.dk/~mailund/suffix_tree.html).
