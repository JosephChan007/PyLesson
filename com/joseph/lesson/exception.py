from com.joseph.lesson import moduleTest


try:
    print(1/0)
except (ZeroDivisionError, NameError) as e:
    print(e)
finally:
    print("sss")

print("ddd")

print(moduleTest)
