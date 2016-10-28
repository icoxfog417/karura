import itertools
from enum import Enum
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif, f_regression
from karura.core.evaluation.base import Evaluation


class ModelSelectionCriteria(Enum):
    f_score = 0
    precision = 1
    recall = 2


class FeatureEvaluation(object):

    def __init__(self, message):
        super().__init__(message)
    
    @classmethod
    def judge(cls, dataset, field_manager, min_feature=3, max_feature=10):
        # evaluate the feature
        best_scenario, best_features = cls.extract_candidates(dataset, field_manager, max_feature)
        
        # todo: comment about features
        message = ""

        return FeatureEvaluation(message)

    @classmethod
    def extract_candidates(cls, dataset, field_manager, max_feature=10, score_threshold=0.6):
        variation = []
        for f in field_manager.features:
            if f.is_categorizable() and not f.category_feature:
                variation.append((f.field_code, False), (f.field_code, True))

        judge_scenarios = itertools.product(*variation)
        criteria = f_classif if field_manager.target.is_categorizable() else f_regression
        best_scenario = None
        best_features = []
        top_score = 0
        for s in judge_scenarios:
            # prepare the feature
            for code, is_category in s:
                field_manager.get_feature(code).category_feature = is_category
            
            # adjust the dataset
            adjusted = field_manager.adjust(dataset)

            # evaluate the feature
            selector = SelectKBest(criteria, k=min(max_feature, len(adjusted.feature_names)))
            selector.fit(adjusted.data, adjusted.target)
            threshold = max(selector.scores_) * score_threshold
            candidates = []
            for i, selected in enumerate(selector.get_support()):
                if selected and selector.scores_[i] > threshold:
                    candidates.append(dataset.feature_names[i])
            
            if sum(selector.scores_) > top_score:
                best_scenario = s
                best_features = candidates
                top_score = sum(selector.scores_)

        # reflect the setting to field_manager
        for code, is_category in best_scenario:
            field_manager.get_feature(code).category_feature = is_category
            field_manager.selected = best_features

        return best_scenario, best_features
