import os
import json
import unittest
from karura.environment import Environment
from karura.core.field_manager import FieldManager
from karura.core.dataset import DataSet


class TestDataSet(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "../data/sample_request.json")

    def test_create_dataset(self):
        env = Environment()
        req = {}
        with open(self.PATH, encoding="utf-8") as req_json:
            req = json.load(req_json)

        manager = FieldManager.read_definitions(req)
        dataset = DataSet.load_dataset(env, manager)
        self.assertTrue(dataset)
        self.assertTrue(dataset.data.shape[0] > 0)
        self.assertTrue(dataset.data.shape[1] > 0)
        self.assertEqual(dataset.data.shape[0], len(dataset.target))
        print(dataset.data.shape)
