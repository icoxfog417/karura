from enum import Enum


class Aspect(Enum):
    dataset = 0
    feature = 1
    model = 2
    system = 3


class Evaluation(Enum):
    message = 0
    praise = 1
    problem = 2


class Message():

    def __init__(self, aspect, message, evaluation=Evaluation.message):
        self.aspect =aspect
        self.message = message
        self.evaluation = evaluation

    @classmethod
    def praise(cls, aspect, message):
        m = cls(aspect, message, Evaluation.praise)

    @classmethod
    def problem(cls, aspect, message):
        m = cls(aspect, message, Evaluation.problem)

