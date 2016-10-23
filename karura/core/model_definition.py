import os
import json


class ModelDefinition():

    def __init__(self, app_id):
        self.app_id = app_id
        self.field_definitions = []
        self.model_class = ""
        self.model = None

    @classmethod
    def make_store_path(cls, app_id):
        model_def = "model_app_{}.modeldef".format(app_id)
        root = os.path.join(os.path.dirname(__file__), "../../store/" + model_def)
        return ""

    @classmethod
    def load(cls, app_id):
        path = cls.make_store_path(app_id)
        with open(path, encoding="utf-8") as md:
            m_def = json.load(md)
            #

    def save(self):
        serialized = {
            "app_id": self.app_id,
            "field_definitions": []
        }

        for fd in self.field_definitions:
            s = fd.to_dict()
            serialized["field_definitions"].append(s)

        return serialized
