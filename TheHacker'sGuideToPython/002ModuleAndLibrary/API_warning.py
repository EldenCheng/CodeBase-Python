"""

当其中一个方法将要被放弃的时候,最好先加一个Warning, 这样用户在新版本的时候就可以见到对应的Warning

"""
import warnings


class WarningTest:

    @staticmethod
    def to_be_deprecation():
        warnings.warn("to_be_deprecation() is going to deprecated, use to_be_implement() instead", DeprecationWarning)
        WarningTest.to_be_implement()

    @staticmethod
    def to_be_implement():
        print("This is correct method!!")

if __name__ == "__main__":
    WarningTest.to_be_deprecation()
