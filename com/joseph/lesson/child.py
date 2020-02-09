from com.joseph.lesson.Father import Father


class Child(Father):
    def __init__(self, name, age, func, work):
        # Father.__init__(self, name, age, func)
        super(Child, self).__init__(name, age, func)
        self.work = work

    # def __str__(self):
    #     return self.name + " " + str(self.age) + " " + self.getFunc() + " " + self.work
    def __str__(self):
        return super().__str__() + " " + self.work


def main():
    c = Child("aaa", 10, "child", "teacher")
    print(c.getFunc())
    c.setFunc("ddd")
    str1 = c.__str__() + " " + c.work
    print(c.__str__())




if __name__ == "__main__":
    main()

