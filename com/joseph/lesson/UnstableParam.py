def _print(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    for arg in args:
        print(arg)
    print("*" * 50)
    for arg in kwargs:
        print(arg, ":", kwargs[arg])


a = (1, 2, 3, 4, 5)
b = {'name': "xw", 'age': "32", "phone": '123'}
_print(*a, *{'b': 12})
# _print(12,34,a=6)
