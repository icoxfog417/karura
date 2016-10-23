import pykintone
import numpy as np


class DataSet():

    def __init__(self, data=(), target=(), feature_names=(), target_name=""):
        self.data = data
        self.target = target
        self.feature_names = feature_names if len(feature_names) > 0 else []
        self.target_name = target_name

    @classmethod
    def load_dataset(cls, env, field_manager=None, app_id="", feature_names=(), target_name=""):
        _app_id = app_id
        _target_name = target_name
        _feature_names = feature_names
        if field_manager:
            _app_id = field_manager.app_id
            _target_name = field_manager.target.field_code
            _feature_names = [f.field_code for f in field_manager.features]
        elif not (app_id and len(feature_names) > 0 and target_name):
            raise Exception("FieldManager or (app_id, feature names, target name) have to be supplied.")

        fields = list(_feature_names) + [_target_name]
        app = pykintone.login(env.kintone_domain, env.kintone_id, env.kintone_password).app(_app_id)

        result = app.select(query="limit 500", fields=fields)  # todo: select all records
        if result.ok:
            data = []
            target = []
            for r in result.records:
                row = []
                for f in _feature_names:
                    v = r[f]["value"]
                    row.append(v)

                t = r[_target_name]["value"]

                data.append(row)
                target.append(t)

            dataset = DataSet(np.array(data), np.array(target), _feature_names, _target_name)
            return dataset

        else:
            raise Exception("error has occured when loading the data {}.".format(result.error))
