import json
import numpy as np
import pykintone
from karura.core.dataset import DataSet


class Field():

    def __init__(self, field_code, field_type="", label="", value_converter=0.0, value_mean=0, value_std=1, category_feature=False):
        self.field_code = field_code
        self.field_type = field_type
        self.label = label
        self.value_converter = value_converter
        self.value_mean = value_mean
        self.value_std = value_std
        self.category_feature = category_feature

    def __call__(self, value):
        if self.category_feature:
            values = value if isinstance(value, (tuple, list)) else [value]
            categories = sorted(self.value_converter, key=self.value_converter.get)
            categorized = [0] * len(categories)
            for i, c in enumerate(categories):
                categorized[i] = 1 if c in values else 0
            return categorized
        else:
            return self._to_feature(value)

    def is_categorizable(self):
        return True if isinstance(self.value_converter, dict) else False
    
    def _to_feature(self, value):
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
            "label": self.label,
            "value_converter": self.value_converter,
            "value_mean": self.value_mean,
            "value_std": self.value_std,
            "category_feature": self.category_feature
        }

    @classmethod
    def load(cls, serialized):
        _s = serialized if isinstance(serialized, dict) else json.loads(serialized)
        return Field(
            _s["field_code"],
            _s["field_type"],
            _s["label"],
            _s["value_converter"],
            _s["value_mean"],
            _s["value_std"],
            _s["category_feature"],
        )


class FieldManager():

    def __init__(self, app_id, features=(), target=None, selected=()):
        self.app_id = app_id
        self.features = features if len(features) > 0 else []
        self.target = target
        self.selected = selected if len(selected) > 0 else []

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
            target = False
            if f is None:
                f = self.get_target(f_code)
                target = True

            if f:
                # todo: have to think about single/multiline text
                f.field_type = forms.raw[f_code]["type"]
                f.label = forms.raw[f_code]["label"]
                if f.field_type in ["RADIO_BUTTON", "DROP_DOWN", "CHECK_BOX", "MULTI_SELECT"]:
                    options = forms.raw[f_code]["options"]
                    f.value_converter = {}
                    for o_k in options:
                        f.value_converter[o_k] = options[o_k]["index"]
                    if not target and f.field_type in ["CHECK_BOX", "MULTI_SELECT"]:
                        f.category_feature = True  # check_box and multi_select have to be category feature

        return self

    def adjust(self, dataset):
        data = None
        target = np.zeros(dataset.target.shape)
        length = dataset.target.shape[0]
        feature_names = []

        for i in list(range(dataset.data.shape[1])) + [-1]:  # -1 is for target
            if i > -1:
                f = self.features[i]
                c = dataset.data[:, i]
            else:
                f = self.target
                c = dataset.target

            converted = np.array(list(map(f.__call__, c))).reshape(length, -1)
            if not f.category_feature:
                f.value_mean = np.mean(converted)
                f.value_std = np.std(converted)
                converted = (converted - f.value_mean) / f.value_std

            column_count = converted.shape[1]

            if i > -1:
                names = []
                if column_count == 1:
                    names = [dataset.feature_names[i]]
                else:
                    for n in range(column_count):
                        names.append("{}_{}".format(dataset.feature_names[i], n))

                for i, n in enumerate(names):
                    if len(self.selected) == 0 or n in self.selected:
                        feature_names.append(n)
                        column = converted[:, i].reshape(-1, 1)
                        if data is None:
                            data = column
                        else:
                            data = np.hstack((data, column))
            else:
                target = converted.flatten()

        dataset = DataSet(data, target, feature_names, dataset.target_name)

        return dataset

    def format(self, code_value_dict):
        pass

    def to_dict(self):
        data_analyzer = {
            "app_id": self.app_id,
            "features": [f.to_dict() for f in self.features],
            "target": self.target.to_dict(),
            "selected": self.selected
        }

        return data_analyzer

    @classmethod
    def load(cls, serialized):
        _s = serialized if isinstance(serialized, dict) else json.loads(serialized)
        app_id = _s["app_id"]
        features = [Field.load(f) for f in _s["features"]]
        target = Field.load(_s["target"])
        selected = _s["selected"]
        return FieldManager(app_id, features, target, selected)
