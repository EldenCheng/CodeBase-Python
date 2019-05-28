class Test():
    d = {}
    @staticmethod
    def get_dict():
        return Test.d
    @staticmethod
    def set_dict(Username):
        Test.d[0]["UserName"] = Username

Test.d = [{"ID": 1001, "UserName": "Leo"}, {"ID": 1002, "UseName": "Elden"}]