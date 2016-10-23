import numpy as np
import pykintone
from karura.core.dataset import DataSet


class Field():

    def __init__(self, field_code, field_type="", value_converter=0.0, value_mean=0, value_std=1):
        self.field_code = field_code
        self.field_type = field_type
        self.value_converter = value_converter
        self.value_mean = value_mean
        self.value_std = value_std

    def __call__(self, value):
        v = value
        if isinstance(self.value_converter, dict):
            if value in self.value_converter:
                v = int(self.value_converter[value])
        elif str(self.value_converter).isdigit():
            v = int(value)
        elif str(self.value_converter).replace(".", "").isdigit():
            v = float(value)

        v = (v - self.value_mean) / self.value_std
        return v

    def to_dict(self):
        return {
            "field_code": self.field_code,
            "field_type": self.field_type,
            "value_converter": self.value_converter,
            "value_mean": self.value_mean,
            "value_std": self.value_std
        }

    @classmethod
    def load(cls, serialized):
        return Field(
            serialized["field_code"],
            serialized["field_type"],
            serialized["value_converter"],
            serialized["value_mean"],
            serialized["value_std"]
        )


class FieldManager():

    def __init__(self, app_id, features=(), target=None):
        self.app_id = app_id
        self.features = features if len(features) > 0 else []
        self.target = target

    @classmethod
    def read_definitions(cls, ml_definitions):
        app_id = ml_definitions["app_id"]
        features = []
        target = None
        for fk in ml_definitions["fields"]:
            fd = ml_definitions["fields"][fk]
            if int(fd["usage"]) == 0:
                features.append(Field(fk))
            elif int(fd["usage"]) == 1:
                target = Field(fk)

        return cls(app_id, features, target)

    def get_feature(self, field_code):
        field = [f for f in self.features if f.field_code == field_code]
        return None if len(field) == 0 else field[0]

    def get_target(self, field_code):
        return None if self.target.field_code != field_code else self.target

    def init(self, env):
        app = pykintone.login(env.kintone_domain, env.kintone_id, env.kintone_password).app(self.app_id)
        forms = app.administration().form().get()
        feature_codes = [f.field_code for f in self.features]

        for f_code in forms.raw:
            f = self.get_feature(f_code)
            if f is None:
                f = self.get_target(f_code)

            if f:
                f.field_type = forms.raw[f_code]["type"]
                # todo: "CHECK_BOX", "MULTI_SELECT"
                if f.field_type in ["RADIO_BUTTON", "DROP_DOWN"]:
                    options = forms.raw[f_code]["options"]
                    f.value_converter = {}
                    for o_k in options:
                        f.value_converter[o_k] = options[o_k]["index"]

        return self

    def adjust(self, dataset):
        data = np.zeros(dataset.data.shape)
        target = np.zeros(dataset.target.shape)

        for i in list(range(dataset.data.shape[1])) + [-1]:
            if i > -1:
                f = self.features[i]
                c = dataset.data[:, i]
            else:
                f = self.target
                c = dataset.target

            converted = np.array(list(map(f.__call__, c)))
            f.value_mean = np.mean(converted)
            f.value_std = np.std(converted)
            normalized = (converted - f.value_mean) / f.value_std

            if i > -1:
                data[:, i] = normalized
            else:
                target = normalized

        dataset = DataSet(data, target, dataset.feature_names, dataset.target_name)

        return dataset

    def format(self, record):
        pass

    def to_dict(self):
        data_analyzer = {
            "app_id": self.app_id,
            "features": [f.to_dict() for f in self.features],
            "target": self.target.to_dict()
        }

        return data_analyzer

    @classmethod
    def load(cls, serialized):
        app_id = serialized["app_id"]
        features = [Field.load(f) for f in serialized["features"]]
        target = Field.load(serialized["target"])
        return FieldManager(app_id, features, target)
