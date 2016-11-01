# -*- coding: utf-8 -*-
from sklearn.svm import SVC, SVR
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from karura.core.evaluation import Message, Aspect, Evaluation


class ModelBuilder():

    def __init__(self, field_manager):
        self.field_manager = field_manager
        self.model = None
        self.model_score = 0
        self._messages = []

    def build(self, dataset):
        evaluators = []
        cv = 5  # todo: have to adjust to dataset size

        if self.field_manager.target.is_categorizable():
            parameter_candidates = [
                {"kernel": ["linear"], "C": [1, 10, 100]},
                {"kernel": ["rbf"], "gamma": [1e-1, 1e-2, 1e-3, 1e-4], "C": [1, 10, 100]}
            ]
            # todo: have to think about scoring parameter (default is accuracy, so f1 related score may be appropriate)
            evaluator = GridSearchCV(
                SVC(C=1),
                parameter_candidates,
                cv=cv
            )
            evaluators.append(evaluator)
        else:

            evaluator1 = GridSearchCV(
                linear_model.ElasticNet(),
                {"alpha": [0.1, 0.5, 0.7, 1], "l1_ratio": [(r + 1) / 10 for r in range(10)]},
                cv=cv
            )

            parameter_candidates = [
                {"kernel": ["rbf"], "gamma": [1e-3, 1e-4], "C": [1, 10, 100]}
            ]

            # todo: have to think about scoring parameter (default is accuracy, so f1 related score may be appropriate)
            evaluator2 = GridSearchCV(
                SVR(C=1),
                parameter_candidates,
                cv=cv
            )
            evaluators.append(evaluator1)
            evaluators.append(evaluator2)

        self.model_score = 0
        self.model = None
        for e in evaluators:
            e.fit(dataset.data, dataset.target)
            if e.best_score_ > self.model_score:
                self.model_score = e.best_score_
                self.model = e.best_estimator_

    def evaluate(self):
        evaluations = []
        if self.model_score < 0.7:
            evaluations.append(
                Message(Aspect.model, "モデルの精度が7割以下({0:.3f})と、あまりよくありません。予測に使う項目を見直すか、もっとデータが必要です。".format(self.model_score))
            )
        elif self.model_score >= 0.8:
            evaluations.append(
                Message.praise(Aspect.model, "モデルの精度は良い感じです！({0:.3f})。十分に予測に使えるでしょう。".format(self.model_score))
            )

        return evaluations
