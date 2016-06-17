from sourcegraph import *

import unittest

class TestSourcegraphAlfred(unittest.TestCase):

    def test_get_posts_type_list(self):
        self.assertEqual(type(get_posts("http")), list)


if __name__ == '__main__':
    unittest.main()
