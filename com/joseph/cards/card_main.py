from com.joseph.cards import card_tool

while True:

    card_tool.show_menu()
    select = input("请选择要进行的操作：")

    if '1' == select:
        card_tool.new_card()

    elif '2' == select:
        card_tool.show_all()

    elif '3' == select:
        card_tool.search_card()

    elif '0' == select:
        break
    else:
        print("选择错误，请重新输入")

print("已退出卡片管理系统，欢迎下次光临！")
