import json
import os
import re
import time
from datetime import datetime, timezone
from decimal import Decimal

dataFile = "data.json"
iQuit = ["0", "q", "退出", "quit"]
sorts = {"1": "吃喝","2": "玩乐", "3": "衣", "4": "住", "5": "行", "0": "其他"}
dateFormat = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%Y年%m月%d日",
    "%Y%m%d",
    "%y-%m-%d",
    "%y/%m/%d",
    "%y.%m.%d",
    "%y年%m月%d日",
    "%y%m%d"
]
slections = {
    "1": ["ID", "i"],
    "2": ["日期", "d"],
    "3": ["类别", "s"],
    "4": ["备注", "m"]
}

#定义数据存取
def saveData(accs):
    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(accs, f, ensure_ascii = False, indent = 4)
def loadData():
    if not os.path.exists(dataFile):
        return []
    with open(dataFile, "r", encoding = "utf-8") as f:
        return json.load(f)

#SNAKKKKK
def snake():
    print("没有账目，但是你发现了一条小蛇/Snake Only")
    print("see,snake:b\n(   )\n(   )\n(. .)")

#金额数校验
def validNum(n):
    expe = r'^-?\d+(\.\d{1,2})?$' #正则：整数或一/两位小数
    if re.match(expe, n):
        try:
            Decimal(n)
            goOn = True
            return goOn
        except ValueError:
            pass
    goOn = False
    return goOn
#金额格式化
def formatAmount(n):
    return n.quantize(Decimal('0.01'))

#时间校验与自动修正
def validTime(t):
    for fmt in dateFormat:
        try:
            dt = datetime.strptime(t, fmt) # noqa: DTZ007
            return dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
    return False

#查账选项校验与格式化
def checkSlection(way, slec):
    #反向映射构建
    reverseMap = {}
    for key, values in slec.items():
        for value in values:
            reverseMap[value] = key
    if way in slec:
        goOn = True
        return way, goOn
    elif way in reverseMap:
        goOn = True
        return reverseMap[way], goOn
    goOn = False
    return way, goOn

#获得，校验并format word2find
def word2find_check(way, word, q, accs):
    while True:
        if way == "4":
            print("可选: 1. 吃喝 2. 玩乐 3.衣 4.住 5.行 0.其他")
        word = input(q).strip()
        if way == "1":
            if isinstance(word, int) and any(d.get('id') == word for d in accs):
                break
    #金额、日期、种类校验并转换:复用之前新账 种类逻辑，部分金额、日期逻辑
        elif way == "2" and validTime(word):
            word = validTime(word)
            break
        elif way == "3":
            goOn = validNum(word)
            if goOn:
                word = Decimal(word)
                word = str(formatAmount(word))
                break
        elif way == "4":
            if word in sorts:
                word = sorts[word]
                break
            elif word in sorts.values():
                break
        print("您再斟酌斟酌？")
        time.sleep(0.5)
    return word

#拆分并优化查账部分逻辑为方法便于复用
def getAccount(way, word, resu, accs):
    resu = []
    for a in accs:
        if way == "1" and word == str(a['id']) or way== "2" and word == str(a['date']) or way == "3" and word == str(a['amount']) or way == "4" and word == str(a['sort']) or way == "5" and word == str(a['mark']):
            resu.append(a)
    return resu

#全匹配删除，从accounts由result所有
def delAccount(resu, accs):
    accs = [a for a in accs if a not in resu]
    return accs

#显示账目方法（通用）
def showAccount(a):
    income = 0
    expand = 0
    balance = 0
    print("-" * 44)
    print(f"{'ID':<8} {'日期':<10} {'类别':<4} {'金额':<8} {'备注':<8}")
    print("-" * 44)
    if not a:
        print("空空如也，记笔账吧。")
        income = expand = balance = "N/A"
    else:
        for i in a:
            print(f"{i['id']:<4}{i['date']:<10}{i['sort']:<8}{i['amount']:<8}{i['mark']:<8}")
            amt = Decimal(i['amount'])
            if amt > 0:
                income += amt
            elif amt < 0:
                expand += Decimal(abs(amt))
        balance = income - expand
    print("-" * 44)
    print(f"总计:收入{income} 支出{expand} 结余{balance}")

def mainMenu():#主菜单
    accounts = loadData()
    while True:
        print("=" * 44)
        print("钱都去哪了?")
        print("=" * 44)
        print("1.新账(n) 2.阅账(v) 3.查账(f)\n4.划账(d) 5.统账(c) 6.改账(e)\n0.合账(q)")
        print("=" * 44)
        goToMenu = str(input("掌柜的，怎么说？"))

#新账
        if goToMenu == "1" or goToMenu == "n":
            while True:
                print("纸笔已备好，请！")

                while True:#金额
                    amount = str(input("金额: ").strip())
                    goOn = validNum(amount)
                    if goOn:
                        amount = Decimal(amount)
                        amount = str(formatAmount(amount))
                        break
                    else:
                        print("掌柜的，", end = "", flush = False)
                        time.sleep(0.1)
                        print("这数不对吧")

                while True:#类别
                    sort = str(input("可选: 1. 吃喝 2. 玩乐 3.衣 4.住 5.行 0.其他\n类别: "))         
                    if sort in sorts:
                        sort = sorts[sort]
                        break
                    elif sort in sorts.values():
                        break
                    else:
                        print("请掌柜的再斟酌")
                        time.sleep(0.5)

                mark = str(input("备注(默认“N/A”): ").strip())#备注
                if mark == "":
                    mark = "N/A"

                while True:#时间
                    date = str(input("时间(年-月-日，默认当天): ").strip())
                    if date == "":
                        date  = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                        break
                    if validTime(date):
                        date = validTime(date)
                        break
                    print("不支持的格式。")
                    print("您再斟酌斟酌？")
                    time.sleep(0.5)

                newID = max([r["id"] for r in accounts], default = 0) + 1#ID

                account = {
                    "id" : newID,
                    "sort" : sort,
                    "amount" : amount,
                    "mark" : mark,
                    "date" : date
                }
                
                #录入账目
                accounts.append(account)
                saveData(accounts)
                loadData()
                
                if len(accounts) == 1:
                    print("记录是掌握生活的开始！")
                    time.sleep(0.5)
                print("记账成功。", end = "", flush = True)
                while True:
                    goOn = input("再记一笔？(y/n)")
                    if goOn == "y":
                        continue
                    elif goOn == "n":
                        break

#阅账 Issue:账目格式/排版
        elif goToMenu == "2" or goToMenu == "v":
            showAccount(accounts)
            while True:
                y = input("回到主菜单？(y)")
                if y == "y":
                    break

#查账
        elif goToMenu == "3" or goToMenu == "f":
            way2find = ""
            while True:
                print("-" * 19, "查账", "-" * 19)
                print("以何为规？")
                print("可选：1. ID(i) 2. 日期(d) 3. 金额(a)\n4.类别(s) 5. 备注(m) 0.退出(q)" ) 
                way2find = input("您的选择？").strip()
                if way2find in iQuit:
                    break 
                way2find, goOn = checkSlection(way2find, slections)
                if goOn == False:
                    print("目前只支持以上选项哦。")
                    continue

                quiz = "用于查询的关键词："
                word2find = 0
                word2find = word2find_check(way2find, word2find, quiz, accounts)

                result = {}
                getAccount(way2find, word2find, result, accounts)
                if len(result) == 0:
                    snake()
                else:
                    print(f"共找到{len(result)}条账目，立刻供上。")
                    time.sleep(0.5)
                    showAccount(result)

            if way2find not in iQuit:
                goOn = input("还查账吗？(y)")
                if goOn == "y":
                    continue

#划账
        elif goToMenu == "4" or goToMenu == "d":
            way2find = ""
            while True:
                if len(accounts) == 0:
                    print("还没记呢，比脸还白的账本还要划。怎地，要画画么？")
                    break
                print("-" * 19, "划账", "-" * 19)
                print("依甚划账？")
                print("可选：1. ID(i) 2. 日期(d) 3. 金额(a)\n4.类别(s) 5. 备注(m) 0.退出(q)" ) 
                way2find = input("您的选择？").strip()
                if way2find in iQuit:
                    break 
                way2find, goOn = checkSlection(way2find, slections)
                if goOn == False:
                    print("目前只支持以上选项哦。")
                    continue

                quiz = "用于划账的关键词："
                word2find = 0
                word2find = word2find_check(way2find, word2find, quiz, accounts)
                #issue:如果用户在word2find想退出(到上一步?)。考虑iQuit

    #加入先让人过一眼要删除的y/n再删除
                result = 0
                result = getAccount(way2find, word2find, result, accounts)
                if len(result) == 0:
                    snake()
                    time.sleep(0.1)
                    break
                else:
                    print(f"已寻找到{len(result)}条账目")

                if way2find == "1":
                    accounts = [a for a in accounts if a['id'] != int(word2find)]
                else:
                    if input("静默划账(y)？(默认展示)").strip() != "y":
                        showAccount(result)
                        if input("确认要划账吗(y)？").strip() != "y":
                            break
                    accounts = delAccount(result, accounts)
                saveData(accounts)
                loadData()

            if way2find not in iQuit:
                time.sleep(0.2)
                goOn = input("再划？(y)")
                if goOn == "y":
                    continue

#统计筛选
        elif goToMenu == "5" or goToMenu == "c" or goToMenu == "6" or goToMenu == "e":
            pass

#合账-退出
        elif goToMenu in iQuit:
            print("彳", end = "", flush = True)
            time.sleep(0.4)
            print("亍，", end = "", flush = True)
            time.sleep(0.3)
            print("那就这样吧先。")
            break
#这不对。
        else:
            print("这不对吧，", end = "", flush = True)
            time.sleep(0.4)
            print("这对", end = "", flush = True)
            time.sleep(0.5)
            print(".", end = "", flush = True)
            time.sleep(0.2)
            print(".", end = "", flush = True)
            time.sleep(0.3)
            print(".", end = "", flush = True)
            time.sleep(0.4)
            print("吗？")
            time.sleep(0.7)

if __name__ == "__main__": mainMenu()
