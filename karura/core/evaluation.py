# -*- coding: utf-8 -*-
from enum import Enum


class Aspect(Enum):
    dataset = 0
    feature = 1
    model = 2
    system = 3

    def __str__(self):
        if self.value == Aspect.dataset.value:
            return "データについて"
        elif self.value == Aspect.feature.value:
            return "予測に使用する項目について"
        elif self.value == Aspect.model.value:
            return "モデルについて"
        elif self.value == Aspect.system.value:
            return "システムエラー"


class Evaluation(Enum):
    message = 0
    praise = 1
    problem = -1


class Message():

    def __init__(self, aspect, message, evaluation=Evaluation.message):
        self.aspect =aspect
        self.message = message
        self.evaluation = evaluation

    @classmethod
    def praise(cls, aspect, message):
        m = cls(aspect, message, Evaluation.praise)
        return m

    @classmethod
    def problem(cls, aspect, message):
        m = cls(aspect, message, Evaluation.problem)
        return m
    
    def __str__(self):
        evaluation_label = "-"
        if self.evaluation == Evaluation.praise:
            evaluation_label = "o"
        else:
            evaluation_label = "x"

        return "{}->({}): {}".format(self.aspect.name, evaluation_label, self.message)
