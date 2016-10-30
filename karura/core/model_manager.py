# -*- coding: utf-8 -*-
import os
import json
from sklearn.externals import joblib
from karura.core.dataset import DataSet
from karura.core.field_manager import FieldManager
from karura.core.feature_builder import FeatureBuilder
from karura.core.evaluation import Evaluation


class ModelManager():
    ROOT = os.path.join(os.path.dirname(__file__), "../../store")
    FIELD_MANAGER_FILE = "field_manager.json"
    MODEL_INFO_FILE = "model_info.json"
    MODEL_FILE = "model.pkl"

    def __init__(self, field_manager=None, trained_model=None):
        self.field_manager = field_manager
        self.model = trained_model
        self._messages = []

    def predict(self, code_value_dict):
        formatted = self.field_manager.format(code_value_dict)
        predicted = self.model.predict(formatted)
        return predicted

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
        
        trained_model = joblib.load(cls.MODEL_FILE)
                    
        model_manager = ModelManager(field_manager, trained_model)

        return model_manager

    def save(self):
        home_dir = cls.__home_dir(self.field_manager.app_id)
        if not os.path.isdir(home_dir):
            os.mkdir(home_dir)

        path_fieldm = os.path.join(home_dir, self.FIELD_MANAGER_FILE)
        with open(path_fieldm, mode="w", encoding="utf-8") as fm:
            serialized = self.field_manager.to_dict()
            json.dump(serialized, fm, indent=2)

        if self.model:
            joblib.dump(self.model, self.MODEL_FILE) 
