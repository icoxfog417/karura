from karura.core.evaluation.base import Evaluation


class DatasetEvaluation(Evaluation):

    def __init__(self, message):
        super().__init__(message)
    
    @classmethod
    def judge(cls, dataset):
        if dataset.data.shape[0] < 50:
            return cls("データ量が少なすぎます。最低でも50件以上はデータがあったほうが良いです。")
        else:
            return None
