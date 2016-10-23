import os
import json


class Environment(object):

    def __init__(self, config_file=""):
        self.kintone_domain = ""
        self.kintone_id = ""
        self.kintone_password = ""

        config_file = config_file
        if not config_file:
            default_path = os.path.join(os.path.dirname(__file__), "../env.json")
            if os.path.isfile(default_path):
                config_file = default_path

        try:
            if config_file:

                with open(config_file, encoding="utf-8") as cf:
                    body = json.load(cf)
                    jget = lambda k, default="": default if k not in body else body[k]

                    self.kintone_domain = jget("kintone_domain")
                    self.kintone_id = jget("kintone_id")
                    self.kintone_password = jget("kintone_password")
            else:
                self.kintone_domain = os.environ.get("KINTONE_DOMAIN", "")
                self.kintone_id = os.environ.get("KINTONE_ID", "")
                self.kintone_password = os.environ.get("KINTONE_PASSWORD", "")

        except Exception as ex:
            raise Exception("environment is not set. please confirm env.json on your root or environment variables")

    @classmethod
    def get_kintone_service(cls, env=None):
        from pykintone.account import Account, kintoneService
        env = env if env else Environment()
        account = Account(env.kintone_domain, env.kintone_id, env.kintone_password)
        service = kintoneService(account)
        return service


    def __str__(self):
        result = self.kintone_domain + " {0}/{1}".format(self.kintone_id, self.kintone_password)
        return result
