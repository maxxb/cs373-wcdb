import unittest
from search import query

class SearchTests(unittest.TestCase):
    """
    Tests for the search functionality.
    This is testing against the index, which is built once
    and is independent of the actual data in the database
    """
    def test_query1(self):
        actual1 = [x for x in query("bill+gates")]
        actual2 = [x for x in query("BILL+GATES")]
        actual3 = [x for x in query(" !#@$   BILL   +    GATES \n ")]
        expected = ['http://tcp-connections.herokuapp.com/organizations/5/', 
                    'http://tcp-connections.herokuapp.com/crises/8/', 
                    'http://tcp-connections.herokuapp.com/crises/1/', 
                    'http://tcp-connections.herokuapp.com/people/4/', 
                    'http://tcp-connections.herokuapp.com/people/7/']
        self.assertEquals(actual1, expected)
        self.assertEquals(actual2, expected)
        self.assertEquals(actual3, expected)

    def test_query2(self):
        actual = [x for x in query("al+gore")]
        expected = ['http://tcp-connections.herokuapp.com/people/7/', 
                    'http://tcp-connections.herokuapp.com/people/10/']
        self.assertEquals(actual, expected)
    
    def test_query3(self):
        actual1 = [x for x in query("")]
        actual2 = [x for x in query("+")]
        actual3 = [x for x in query("!@#$%^&*()")]
        actual4 = [x for x in query("          ")]
        self.assertEquals(actual1, [])
        self.assertEquals(actual2, [])
        self.assertEquals(actual3, [])
        self.assertEquals(actual4, [])

    def test_query4(self):
        actual = [x for x in query("bp")]
        expected = ['http://tcp-connections.herokuapp.com/crises/7/', 
                    'http://tcp-connections.herokuapp.com/organizations/10/']
        self.assertEquals(actual, expected)

    def test_query5(self):
        actual1 = [x for x in query("bp+oil")]
        actual2 = [x for x in query("oil+bp")]
        expected = ['http://tcp-connections.herokuapp.com/crises/7/', 
                    'http://tcp-connections.herokuapp.com/organizations/10/']
        self.assertEquals(actual1, expected)
        self.assertEquals(actual2, expected)

    def test_query6(self):
        actual = [x for x in query("oil")]
        expected = ['http://tcp-connections.herokuapp.com/crises/7/', 
                    'http://tcp-connections.herokuapp.com/organizations/10/']
        self.assertEquals(actual, expected)

if __name__ == '__main__':
    unittest.main()
