card_list = []


def show_menu():
    """显示菜单"""
    print("*" * 50)
    print("欢迎使用【卡片管理系统】V1.0")
    print("")
    print("1. 新增卡片")
    print("2. 显示卡片")
    print("3. 搜索卡片")
    print("")
    print("0. 退出系统")
    print("*" * 50)


def new_card():
    """新增名片"""
    print("新增名片")
    name = input("请输入姓名：")
    phone = input("请输入手机号：")
    qq = input("请输入QQ号：")
    email = input("请输入邮箱：")
    card_info = {'姓名': name, '手机': phone, 'QQ': qq, '邮箱': email}
    card_list.append(card_info)
    show_all()


def show_all():
    """显示所有名片"""
    print("显示所有名片")
    if len(card_list) > 0:
        print("%s\t\t%s\t\t%s\t\t%s" % ("姓名", "手机", "扣扣", "邮箱"))
        print("=" * 50)
        for card in card_list:
            print("%s\t\t%s\t\t%s\t\t%s" % (card["姓名"], card["手机"], card["QQ"], card["邮箱"]))
    else:
        print("无名片可以展示...")


def search_card():
    """搜索名片"""
    print("搜索名片")
    name = input("请输入要查询的姓名：")
    for card in card_list:
        if card["姓名"] == name:
            print("%s\t\t%s\t\t%s\t\t%s" % ("姓名", "手机", "扣扣", "邮箱"))
            print("=" * 50)
            print("%s\t\t%s\t\t%s\t\t%s" % (card["姓名"], card["手机"], card["QQ"], card["邮箱"]))
            print("=" * 50)

            detail_card(card)

            break
    else:
        print("未找到要查询的姓名0：%s" % name)


def detail_card(card):
    while True:
        select = input("请选择要进行的操作【1：删除；2：修改；0：返回】: ")
        if '0' == select:
            break
        elif '1' == select:
            card_del(card)
        elif '2' == select:
            card_edit(card)
        else:
            print("选择错误，请重新输入")


def card_del(card):

    """
    删除卡片
    :param card: 卡片
    :return: 无
    """
    card_list.remove(card)


def card_edit(card):

    """
    修改卡片
    :param name: 卡片
    :return: 无
    """
    card["姓名"] = process_inpur(card["姓名"], "请输入姓名：")
    card["手机"] = process_inpur(card["手机"], "请输入手机号：")
    card["QQ"] = process_inpur(card["QQ"], "请输入QQ号：")
    card["邮箱"] = process_inpur(card["邮箱"], "请输入邮箱：")


def process_inpur(init, txt):
    content = input(txt)
    if len(content) > 0:
        return content
    else:
        return init

