import unittest
from karura.environment import Environment


class TestEnvironment(unittest.TestCase):

    def test_environment(self):
        # have to prepare env.json
        env = Environment()
        self.assertTrue(env.kintone_domain)
        self.assertTrue(env.kintone_id)
        self.assertTrue(env.kintone_password)
        print(env)
