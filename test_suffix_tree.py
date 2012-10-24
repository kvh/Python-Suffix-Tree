import unittest
from suffix_tree import SuffixTree


class SuffixTreeTest(unittest.TestCase):
    """Some functional tests.
    """
    def test_empty_string(self):
        st = SuffixTree('')
        self.assertEqual(st.find_substring('not there'), -1)
        self.assertEqual(st.find_substring(''), -1)
        self.assertFalse(st.has_substring('not there'))
        self.assertFalse(st.has_substring(''))
        
    def test_repeated_string(self):
        st = SuffixTree("aaa")
        self.assertEqual(st.find_substring('a'), 0)
        self.assertEqual(st.find_substring('aa'), 0)
        self.assertEqual(st.find_substring('aaa'), 0)
        self.assertEqual(st.find_substring('b'), -1)
        self.assertTrue(st.has_substring('a'))
        self.assertTrue(st.has_substring('aa'))
        self.assertTrue(st.has_substring('aaa'))
        
        self.assertFalse(st.has_substring('aaaa'))
        self.assertFalse(st.has_substring('b'))
        #case sensitive by default
        self.assertFalse(st.has_substring('A'))
        
    def test_long_string(self):
        f = open("test.txt")
        st = SuffixTree(f.read())
        self.assertEqual(st.find_substring('Ukkonen'), 1498)
        self.assertEqual(st.find_substring('Optimal'), 11131)
        self.assertFalse(st.has_substring('ukkonen'))
        
    def test_case_sensitivity(self):
        f = open("test.txt")
        st = SuffixTree(f.read(), case_insensitive=True)
        self.assertEqual(st.find_substring('ukkonen'), 1498)
        self.assertEqual(st.find_substring('Optimal'), 1830)

    def test_repr(self):
        st = SuffixTree("t")
        output = '\tStart \tEnd \tSuf \tFirst \tLast \tString\n\t0 \t1 \t-1 \t0 \t0 \tt\n'
        import pdb;pdb.set_trace()
        self.assertEqual(st.__repr__(), output)

if __name__ == '__main__':
    unittest.main()

