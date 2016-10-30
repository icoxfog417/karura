import unittest
import numpy as np
from sklearn import datasets
from karura.core.dataset import DataSet
from karura.core.feature_builder import FeatureBuilder
from karura.core.field_manager import Field, FieldManager


class TestFeatureBuilder(unittest.TestCase):

    def test_feature_extraction(self):
        dataset, field_manager = self.make_dataset_and_field_manager()
        f_builder = FeatureBuilder(field_manager)
        f_builder.build(dataset)
        self.assertTrue(len(f_builder._best_features) < len(dataset.feature_names))

    def make_dataset_and_field_manager(self):
        iris = datasets.load_iris()
        dataset = DataSet(iris.data, iris.target, iris.feature_names, iris.target_names)

        feature_fields = []
        for i, name in enumerate(dataset.feature_names):
            f = Field(name, "NUMBER", value_mean=np.mean(dataset.data[:, i]), value_std=np.std(dataset.data[:, i]))
            feature_fields.append(f)

        target = Field("flower kind", "DROP_DOWN", value_converter={"setosa": 0, "versicolor": 1, "virginica": 2})
        field_manager = FieldManager(-1, feature_fields, target)

        return dataset, field_manager
