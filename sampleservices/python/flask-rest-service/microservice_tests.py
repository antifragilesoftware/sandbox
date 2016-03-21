import os
import microservice
import unittest
import tempfile

class MicroserviceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = microservice.app.test_client()

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Hello!' in rv.data
        
if __name__ == '__main__':
    unittest.main()