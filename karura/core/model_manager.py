# -*- coding: utf-8 -*-
import os
import json
from sklearn.externals import joblib
from karura.core.dataset import DataSet
from karura.core.field_manager import FieldManager
from karura.core.feature_builder import FeatureBuilder
from karura.core.model_builder import ModelBuilder
from karura.core.evaluation import Evaluation


class ModelManager():
    ROOT = os.path.join(os.path.dirname(__file__), "../../store")
    FIELD_MANAGER_FILE = "field_manager.json"
    MODEL_FILE = "model.pkl"

    def __init__(self, field_manager=None, trained_model=None):
        self.field_manager = field_manager
        self.model = trained_model
        self.model_score = 0
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

    def build(self, environment, ml_definitions):
        self._messages.clear()

        # read received definitions and configure these
        field_manager = FieldManager.read_definitions(ml_definitions)
        field_manager.init(environment)

        # load dataset and evaluate
        dataset = DataSet.load_dataset(environment, field_manager=field_manager)
        self._merge_and_check_messages(dataset.evaluate())

        # build the feature from field and dataset
        f_builder = FeatureBuilder(field_manager)
        f_builder.build(dataset)
        self._merge_and_check_messages(f_builder.evaluate())

        # adjust the dataset to the feature
        adjusted = f_builder.field_manager.adjust(dataset)

        # make & train the model
        m_builder = ModelBuilder(f_builder.field_manager)
        m_builder.build(adjusted)
        self._merge_and_check_messages(m_builder.evaluate())

        self.field_manager = f_builder.field_manager
        self.model = m_builder.model
        self.model_score = m_builder.model_score

    def get_evaluation(self):
        messages = {}
        for m in self._messages:
            key = str(m.aspect)
            if key not in messages:
                messages[key] = []
            messages[key].append({
                "evaluation": str(m.evaluation),
                "message": m.message
            })
        
        result = {
            "score": "{0:.4f}".format(self.model_score),
            "messages": messages
        }        

        return result

    def predict(self, code_value_dict):
        formatted = self.field_manager.format(code_value_dict)
        predicted = self.model.predict(formatted)
        p = self.field_manager.target.restore(predicted[0])
        return p

    @classmethod
    def __model_name(cls, app_id):
        return "model_for_app_{}".format(app_id)

    @classmethod
    def __home_dir(cls, app_id):
        return os.path.join(cls.ROOT, "./" + cls.__model_name(app_id))

    @classmethod
    def load(cls, app_id):
        home_dir = cls.__home_dir(app_id)
        if not os.path.isdir(home_dir):
            raise Exception("Model File for application {} have not created yet.".format(app_id))

        path_fieldm = os.path.join(home_dir, cls.FIELD_MANAGER_FILE)
        with open(path_fieldm, mode="r", encoding="utf-8") as md:
            serialized = json.load(md)
            field_manager = FieldManager.load(serialized)
        
        trained_model = joblib.load(os.path.join(home_dir, cls.MODEL_FILE))

        model_manager = ModelManager(field_manager, trained_model)

        return model_manager

    def save(self):
        home_dir = self.__home_dir(self.field_manager.app_id)
        if not os.path.isdir(home_dir):
            os.mkdir(home_dir)

        path_fieldm = os.path.join(home_dir, self.FIELD_MANAGER_FILE)
        with open(path_fieldm, mode="w", encoding="utf-8") as fm:
            serialized = self.field_manager.to_dict()
            json.dump(serialized, fm, indent=2)

        if self.model:
            joblib.dump(self.model, os.path.join(home_dir, self.MODEL_FILE))
