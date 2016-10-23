import os
import json
import unittest
from karura.core.field_manager import FieldManager
from karura.core.dataset import DataSet
from karura.environment import Environment


class TestFieldManager(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "../data/sample_request.json")

    def xtest_read_definition(self):
        body = self._read_json()
        manager = FieldManager.read_definitions(body)
        self.assertTrue(manager.app_id)
        self.assertTrue(manager.features)
        self.assertTrue(manager.target)

    def xtest_init_fields(self):
        env = Environment()
        body = self._read_json()
        manager = FieldManager.read_definitions(body).init(env)
        self.assertTrue(manager)

    def test_adjust(self):
        env = Environment()
        body = self._read_json()
        manager = FieldManager.read_definitions(body).init(env)
        dataset = DataSet.load_dataset(env, manager)
        adjusted = manager.adjust(dataset)

        self.assertTrue(adjusted)

    def _read_json(self):
        req = {}
        with open(self.PATH, encoding="utf-8") as req_json:
            req = json.load(req_json)
        return req
