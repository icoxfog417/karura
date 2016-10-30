# -*- coding: utf-8 -*-
import pykintone
import numpy as np
from karura.core.evaluation import Aspect, Message


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

        result = app.select(query="limit 500", fields=fields)  # todo: get over 500 records
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
            if dataset.data[0] != len(dataset.target):
                raise Exception("Size mismatch occurrs at data and target")

            return dataset

        else:
            raise Exception("error has occured when loading the data {}.".format(result.error))

    def evaluate(self):
        evaluations = []
        if self.data.shape[0] < 50:
            evaluations.append(
                Message.problem(Aspect.dataset, "データ量が少なすぎます。最低でも50件以上はデータがあったほうが良いです。")
            )
        if self.data.shape[0] < self.data.shape[1]:
            evaluations.append(
                Message.problem(Aspect.dataset, "予測に使う項目数に対して、データ量が少なすぎます。予測項目を少なくするか、もっとデータを用意しましょう。")
            )

        return evaluations
