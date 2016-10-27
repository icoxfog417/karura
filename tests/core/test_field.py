import os
import json
import unittest
from karura.core.field_manager import Field, FieldManager


class TestField(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "../data/sample_request.json")
    
    def test_category_field(self):
        category_field = Field("category", "RADIO_BUTTON", value_converter={"A": 1, "B":2, "C":3}, category_feature=True)
        v = category_field("B")
        self.assertEqual(3, len(v))  # data is like (A, B, C) = (0, 1, 0)
        self.assertEqual(1, v[1])

    def test_serialize(self):
        field = Field("test_field", "SINGLE_TEXT", {"XX": 1}, 1, 2, True)
        d = field.to_dict()
        serialized = json.dumps(d)
        loaded = Field.load(serialized)
        d2 = loaded.to_dict()
        
        for k in d:
            self.assertEqual(d[k], d2[k])

    def test_field_manager_serialization(self):
        feature1 = Field("test_field", "CHECK_BOX", {"X": 1, "Y": 2}, category_feature=True)
        feature2 = Field("test_field2", "NUMBER", value_mean=1, value_std=2)
        target = Field("test_target", "RADIO_BUTTON", {"A": 1, "B": 2}, category_feature=True)

        manager = FieldManager(1, [feature1, feature2], target)
        d = manager.to_dict()
        serialized = json.dumps(d)
        loaded_manager = FieldManager.load(serialized)
        d2 = loaded_manager.to_dict()

        for k in d:
            self.assertEqual(d[k], d2[k])
