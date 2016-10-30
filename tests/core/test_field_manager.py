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

        # load
        adjusted = manager.adjust(dataset)
        self.assertEqual(dataset.data.shape, adjusted.data.shape)
        self.compare_adjusted_and_format(manager, adjusted, dataset)

        # with category variable
        manager.get_feature("direction").category_feature = True
        adjusted = manager.adjust(dataset)
        self.assertTrue(dataset.data.shape[1] < adjusted.data.shape[1])
        self.assertEqual(adjusted.data.shape[1], len(adjusted.feature_names))
        self.compare_adjusted_and_format(manager, adjusted, dataset)

        # select feature
        manager.selected = ["walk_time", "area", "direction_0", "direction_4"]
        adjusted = manager.adjust(dataset)
        self.assertEqual(adjusted.data.shape[1], 4)
        self.compare_adjusted_and_format(manager, adjusted, dataset)

        # restore from serialized
        serialized = json.dumps(manager.to_dict())
        loaded_manager = FieldManager.load(serialized)
        adjusted_from_loaded = loaded_manager.adjust(dataset)
        self.assertEqual(adjusted.data.shape, adjusted_from_loaded.data.shape)
        self.compare_adjusted_and_format(manager, adjusted_from_loaded, dataset)

    def compare_adjusted_and_format(self, manager, adjusted, dataset):
        code_value_dict = {}
        target_index = 0
        for i, name in enumerate(dataset.feature_names):
            code_value_dict[name] = dataset.data[target_index][i]
        formatted = manager.format(code_value_dict)

        for av, fv in zip(adjusted.data[target_index], formatted):
            self.assertEqual(av, fv)

    def _read_json(self):
        req = {}
        with open(self.PATH, encoding="utf-8") as req_json:
            req = json.load(req_json)
        return req
