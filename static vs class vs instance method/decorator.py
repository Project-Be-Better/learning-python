class Spam:

    numInstances = 0

    def __init__(self):
        Spam.numInstances = Spam.numInstances + 1

    @staticmethod
    def printNumInstances():
        print("Number of instances created: %s" % Spam.numInstances)


class Methods:

    def instanceMethod(self, x):
        print([self, x])

    @staticmethod
    def staticMethod(x):
        print([x])

    @classmethod
    def classMethod(cls, x):
        print([cls, x])

    @property
    def name(self):
        return "Bob" + self.__class__.__name__


if __name__ == "__main__":

    obj = Methods()

    obj.instanceMethod(1)
    # [<__main__.Methods object at 0x0000023BAEB53190>, 1]

    obj.staticMethod(1)
    # [1]

    obj.classMethod(1)
    # [<class '__main__.Methods'>, 1]

    obj.name


# if __name__ == "__main__":
#     a = Spam()
#     b = Spam()
#     c = Spam()

#     Spam.printNumInstances()
#     # Number of instances created: 3
#     a.printNumInstances()
#     # Number of instances created: 3
