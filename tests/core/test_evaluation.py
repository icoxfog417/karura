# -*- coding: utf-8 -*-
import unittest
from karura.core.evaluation import Message, Aspect, Evaluation
from karura.core.model_manager import ModelManager


class TestEvaluation(unittest.TestCase):

    def test_format(self):
        print(Aspect.model)

    def test_get_evaluations(self):
        praise = Message.praise(Aspect.dataset, "データセットに関する誉め言葉")
        message1 = Message(Aspect.feature, "特徴量に関するコメント")
        message2 = Message(Aspect.feature, "特徴量に関するコメント2")
        problem = Message.problem(Aspect.model, "モデルに何か起こった")
        m_manager = ModelManager()
        
        for m in (praise, message1, message2, problem):
            m_manager._messages.append(m)
        
        m_manager.model_score = 0.8

        result = m_manager.get_evaluation()
        print(result)
        self.assertEqual(0.8, result["score"])
