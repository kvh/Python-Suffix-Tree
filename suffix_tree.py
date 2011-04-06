""" 
Ken Van Haren
krv2@duke.edu

Based off of Mark Nelson's C++ implementation of Ukkonen's algorithm. Ukkonen's
algorithm gives a O(n) + O(k) contruction time for a suffix tree, where n is 
the length of the string and k is the size of the alphabet of that string. 
Ukkonen's is an online algorithm, processing the input sequentially and producing 
a valid suffix tree at each character.
"""

class Node(object):
    """A node in the suffix tree. 
    
    suffix_node
        the index of a node with a matching suffix, representing a suffix link.
        -1 indicates this node has no suffix link.
    
    node_count (static) 
        keeps the count of total nodes in the tree
    """
    def __init__(self):
        self.suffix_node = -1   

    def __repr__(self):
        return "Node(suffix link: %d)"%self.suffix_node

class Edge(object):
    """An edge in the suffix tree.
    
    first_char_index
        index of start of string part represented by this edge
        
    last_char_index
        index of end of string part represented by this edge
        
    source_node_index
        index of source node of edge
    
    dest_node_index
        index of destination node of edge
    """
    def __init__(self, first_char_index, last_char_index, source_node_index, dest_node_index):
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)'% (self.source_node_index, self.dest_node_index 
                                        ,self.first_char_index, self.last_char_index )


class Suffix(object):
    """Represents a suffix from first_char_index to last_char_index.
    
    source_node_index
        index of node where this suffix starts
    
    first_char_index
        index of start of suffix in string
        
    last_char_index
        index of end of suffix in string
    """
    def __init__(self, source_node_index, first_char_index, last_char_index):
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index
                
    def explicit(self):
        """A suffix is explicit if it ends on a node. first_char_index
        is set greater than last_char_index to indicate this."""
        return self.first_char_index > self.last_char_index
    
    def implicit(self):
        return self.last_char_index >= self.first_char_index

        
class SuffixTree(object):
    def __init__(self, string):
        self.string = string
        self.N = len(string) - 1
        self.nodes = [Node()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        for i in range(len(string)):
            self.add_prefix(i)
            
    def add_prefix(self, last_char_index):
        
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.string[last_char_index]) in self.edges:
                    # prefix is already in tree
                    break
            else:
                e = self.edges[self.active.source_node_index, self.string[self.active.first_char_index]]
                if self.string[e.first_char_index + self.active.length + 1] == self.string[last_char_index]:
                    # prefix is already in tree
                    break
                parent_node = self.split_edge(e, self.active)
        

            self.nodes.append(Node())
            e = Edge(last_char_index, self.N, parent_node, len(self.nodes) - 1)
            self.insert_edge(e)
            
            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node
            
            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self.canonize_suffix(self.active)
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self.canonize_suffix(self.active)
        
    
    def find_edge(self, node_index, char):
        return self.edges.get((node_index, char), Edge(None, None, -1, -1))
        
    def insert_edge(self, edge):
        self.edges[(edge.source_node_index, self.string[edge.first_char_index])] = edge
        
    def remove_edge(self, edge):
        self.edges.pop((edge.source_node_index, self.string[edge.first_char_index]))
        
    def split_edge(self, edge, suffix):
        self.nodes.append(Node())
        e = Edge(edge.first_char_index, edge.first_char_index + suffix.length, suffix.source_node_index, len(self.nodes) - 1)
        self.remove_edge(edge)
        self.insert_edge(e)
        self.nodes[e.dest_node_index].suffix_node = suffix.source_node_index  ### need to add node for each edge
        edge.first_char_index += suffix.length + 1
        edge.source_node_index = e.dest_node_index
        self.insert_edge(edge)
        return e.dest_node_index

    def canonize_suffix(self, suffix):
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index, self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self.canonize_suffix(suffix)
 
    def print_(self, curr_index=None):
        if curr_index is None:
            curr_index = self.N
        print "\tStart \tEnd \tSuf \tFirst \tLast \tString"
        values = self.edges.values()
        values.sort(key=lambda x: x.source_node_index)
        for s in values:
            if s.source_node_index == -1:
                continue
            print "\t%s \t%s \t%s \t%s \t%s \t"%(s.source_node_index
                    ,s.dest_node_index 
                    ,self.nodes[s.dest_node_index].suffix_node 
                    ,s.first_char_index
                    ,s.last_char_index),
                    
            
            top = min(curr_index, s.last_char_index)
            print self.string[s.first_char_index:top+1]
    
    def has_substring(self, substring):
        if not substring:
            return True
        curr_node = 0
        i = 0
        while i < len(substring):
            edge = self.edges.get((curr_node, substring[i]))
            if not edge:
                return False
            ln = min(edge.length + 1, len(substring) - i)
            if substring[i:i + ln] != self.string[edge.first_char_index:edge.first_char_index + ln]:
                return False
            i += edge.length + 1
            curr_node = edge.dest_node_index
        return True

if __name__ == '__main__':

    tree = SuffixTree('banana$')
    tree.print_()
        