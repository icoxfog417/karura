import unittest
import os
import json
from karura.environment import Environment
from karura.core.dataset import DataSet
from karura.core.model_manager import ModelManager


class TestModelManager(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "../data/sample_request.json")

    def test_build_model(self):
        env = Environment()
        body = self._read_json()

        m_manager = ModelManager()
        m_manager.build(env, body)
        self.assertTrue(m_manager.model)

        app_id = m_manager.field_manager.app_id
        m_manager.save()
        loaded = ModelManager.load(app_id)
        dataset = DataSet.load_dataset(env, field_manager=loaded.field_manager)
        code_and_value = {}
        for i, f_name in enumerate(dataset.feature_names):
            code_and_value[f_name] = dataset.data[0][i]

        predicted = loaded.predict(code_and_value)
        teacher = dataset.target[0]
        print(predicted)
        print(teacher)

    def _read_json(self):
        req = {}
        with open(self.PATH, encoding="utf-8") as req_json:
            req = json.load(req_json)
        return req
