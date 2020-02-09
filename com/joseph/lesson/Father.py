class Father(object):
    def __init__(self, name, age, func):
        self.name = name
        self.age = age
        self.__func = func

    def setFunc(self, func):
        self.__func = func

    def getFunc(self):
        return self.__func

    def __str__(self):
        return self.name + " " + str(self.age) + " " + self.__func

