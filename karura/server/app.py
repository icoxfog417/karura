import json
import tornado.web
import tornado.escape


class PingHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("welcome.")

    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        self.write(body)


class TrainingHandler(tornado.web.RequestHandler):

    def post(self):
        dummy = {'messages': {
            'データについて': [{'evaluation': '○', 'message': 'データセットに関する誉め言葉'}], 
            'モデルについて': [{'evaluation': '×', 'message': 'モデルに何か起こった'}], 
            '予測に使用する項目について': [{'evaluation': '-', 'message': '特徴量に関するコメント'}, {'evaluation': '-', 'message': '特徴量に関するコメント2'}]
            }, 'score': 0.8}
        self.write(dummy)


class PredictionHandler(tornado.web.RequestHandler):

    def post(self):
        dummy = {
            'prediction': {
                "house_price": 0
            }
        }
        self.write(dummy)


def application(debug=False):
    app = tornado.web.Application(
        [
            (r"/ping", PingHandler),
            (r"/train", TrainingHandler),
            (r"/predict", PredictionHandler)
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        debug=debug,
    )
    return app

