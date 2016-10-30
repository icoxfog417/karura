# -*- coding: utf-8 -*-
from sklearn.svm import SVC
from sklearn import linear_model
from karura.core.dataset import DataSet
from karura.core.field_manager import FieldManager
from karura.core.feature_builder import FeatureBuilder
from karura.core.evaluation import Message, Aspect, Evaluation


class ModelBuilder():

    def __init__(self, env):
        self.env = env
        self._messages = []

    def _check_problem(self, interrupt=True):
        problems = [m for m in self._messages if m.evaluation == Evaluation.problem]
        if len(problems) > 0:
            if interrupt:
                raise Exception("Problem has occured. please see the detail in the _messages.")
            else:
                return True
        else:
            return False

    def _merge_message(self, messages):
        for m in messages:
            self._messages.append(m)

    def _merge_and_check_messages(self, messages, interrupt=True):
        self._merge_message(messages)
        self._check_problem(interrupt)

    def build(self, ml_definitions):
        self._messages.clear()

        # read received definitions and configure these
        field_manager = FieldManager.read_definitions(ml_definitions)
        field_manager.init(self.env)

        # load dataset and evaluate
        dataset = DataSet.load_dataset(self.env, field_manager=field_manager)
        self._merge_and_check_messages(dataset.evaluate())

        # build the feature from field and dataset
        f_builder = FeatureBuilder(field_manager)
        f_builder.build(dataset)
        self._merge_and_check_messages(f_builder.evaluate())

        # adjust the dataset to the feature
        adjusted = f_builder.field_manager.adjust(dataset)

        # make & train the model
        model = self.make_model(adjusted)


    def make_model(self, dataset):
        model = None
        if dataset.target.is_categorizable():
            candidates = [
                SVC(kernel="linear", C=0.025),
                SVC(gamma=2, C=1),
            ]
        else:
            candidates = [
                linear_model.LinearRegression(),
                linear_model.ElasticNet()
            ]



        pass

    def evaluate(self):
        pass
