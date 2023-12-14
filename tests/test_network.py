import unittest
from network import Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.network = Network()

    def test_p(self):
        self.assertIsInstance(self.network.p, str)

    def test_connect(self):
        self.network._connect()
        self.assertIsNotNone(self.network.p)

    def test_send(self):
        response = self.network.send("Hello, server!")
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()