import unittest
import numpy as np
from sklearn import datasets
from karura.core.dataset import DataSet
from karura.core.field_manager import Field, FieldManager
from karura.core.model_builder import ModelBuilder


class TestModelBuilder(unittest.TestCase):

    def test_make_classifier_model(self):
        dataset, field_manager = self.make_cl_dataset_and_field_manager()
        m_builder = ModelBuilder(field_manager)
        m_builder.build(dataset)
        self.assertTrue(m_builder.model)
        print(m_builder.model_score)

    def test_make_regression_model(self):
        dataset, field_manager = self.make_rg_dataset_and_field_manager()
        m_builder = ModelBuilder(field_manager)
        m_builder.build(dataset)
        self.assertTrue(m_builder.model)
        print(m_builder.model_score)

    def make_cl_dataset_and_field_manager(self):
        iris = datasets.load_iris()
        dataset = DataSet(iris.data, iris.target, iris.feature_names, iris.target_names)

        feature_fields = []
        for i, name in enumerate(dataset.feature_names):
            f = Field(name, "NUMBER", value_mean=np.mean(dataset.data[:, i]), value_std=np.std(dataset.data[:, i]))
            feature_fields.append(f)

        target = Field("flower kind", "DROP_DOWN", value_converter={"setosa": 0, "versicolor": 1, "virginica": 2})
        field_manager = FieldManager(-1, feature_fields, target)

        return dataset, field_manager

    def make_rg_dataset_and_field_manager(self):
        boston = datasets.load_boston()
        dataset = DataSet(boston.data, boston.target, boston.feature_names, "price")

        feature_fields = []
        for i, name in enumerate(dataset.feature_names):
            f = Field(name, "NUMBER", value_mean=np.mean(dataset.data[:, i]), value_std=np.std(dataset.data[:, i]))
            feature_fields.append(f)

        target = Field("price", "NUMBER", value_mean=np.mean(dataset.target), value_std=np.std(dataset.target))
        field_manager = FieldManager(-1, feature_fields, target)

        return dataset, field_manager
