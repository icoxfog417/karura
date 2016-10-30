# -*- coding: utf-8 -*-
import itertools
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif, f_regression
from karura.core.evaluation import Aspect, Message


class FeatureBuilder(object):

    def __init__(self, field_manager):
        self.field_manager = field_manager
        self._best_scenario = []
        self._best_features = {}

    def build(self, dataset, max_feature=10, score_threshold=0.6):
        variation = []
        for f in self.field_manager.features:
            if f.is_categorizable() and not f.category_feature:
                variation.append([(f.field_code, False), (f.field_code, True)])

        judge_scenarios = itertools.product(*variation)
        criteria = f_classif if self.field_manager.target.is_categorizable() else f_regression
        self._best_scenario = []
        self._best_features = {}
        top_score = 0
        for s in judge_scenarios:
            # prepare the feature
            for code, is_category in s:
                self.field_manager.get_feature(code).category_feature = is_category
            
            # adjust the dataset
            adjusted = self.field_manager.adjust(dataset)

            # evaluate the feature
            selector = SelectKBest(criteria, k=min(max_feature, len(adjusted.feature_names)))
            selector.fit(adjusted.data, adjusted.target)
            threshold = max(selector.scores_) * score_threshold
            candidates = {}
            for i, selected in enumerate(selector.get_support()):
                if selected and selector.scores_[i] > threshold:
                    candidates[dataset.feature_names[i]] = selector.scores_[i]
            
            if sum(selector.scores_) > top_score:
                self._best_scenario = s
                self._best_features = candidates
                top_score = sum(selector.scores_)

        # reflect the setting to field_manager
        for code, is_category in self._best_scenario:
            self.field_manager.get_feature(code).category_feature = is_category
            self.field_manager.selected = list(self._best_features.keys())

    def evaluate(self):
        evaluates = []
        if len(self.field_manager.selected) < len(self.field_manager.features) * 0.5:
            evaluates.append(
                Message(Aspect.feature, "予測に使用するとして選択した項目のうち、予測に使えるものがあまりありません")
            )

        return evaluates
