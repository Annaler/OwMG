import json
import os
import re
import time
from datetime import datetime, timedelta
from decimal import Decimal

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
slections1 = {
    "1": ["ID", "i"],
    "2": ["日期", "d"],
    "3": ["类别", "s"],
    "4": ["备注", "m"]
}
slections2 = {
    "1": ["ID", "i"],
    "2": ["日期", "d"],
    "3": ["金额", "a"],
    "4": ["类别", "s"],
}
slections3 = {
    "1": ["sort", "s", "种类"],
    "2": ["amount", "a", "金额"],
    "3": ["mark", "m", "备注"],
    "4": ["date", "d", "日期"],
    "5": ["r", "rewrite", "重写"],
}

#定义数据存取
def saveData(accounts):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii = False, indent = 4)
def loadData():
    if not os.path.exists("data.json"):
        return []
    with open("data.json", "r", encoding = "utf-8") as f:
        return json.load(f)

#SNAKKKKK
def snake():
    print("没有账目，但是你发现了一条小蛇/Snake Only")
    print("see,snake:b\n(   )\n(   )\n(. .)")

#金额数校验
def validNum(amount):
    expe = r'^-?\d+(\.\d{1,2})?$' #正则：整数或一/两位小数
    if re.match(expe, amount):
        try:
            Decimal(amount)
            goOn = True
            return goOn
        except ValueError:
            pass
    goOn = False
    return goOn
#金额格式化
def formatAmount(amount):
    return amount.quantize(Decimal('0.01'))

#时间校验与自动修正
def validTime(date):
    for fmt in dateFormat:
        try:
            dt = datetime.strptime(date, fmt) # noqa: DTZ007
            return dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
    return False

#查账选项校验与格式化
def checkSlection(way2find, slections):
    #反向映射构建
    reverseMap = {}
    for key, values in slections.items():
        for value in values:
            reverseMap[value] = key
    if way2find in slections:
        goOn = True
        return way2find, goOn
    elif way2find in reverseMap:
        goOn = True
        return reverseMap[way2find], goOn
    goOn = False
    return way2find, goOn

#获得，校验并format word2find
def word2find_check(way2find, quiz, accounts):
    inAcc = goOn = False
    while True:
        if way2find == "4":
            print("可选: 1. 吃喝 2. 玩乐 3.衣 4.住 5.行 0.其他")
        word2find = input(quiz).strip()
        if (word2find != "0") and (word2find in iQuit):
            break
        elif way2find == "1":#by ID
            try:
                int(word2find)
                goOn = True
            except ValueError:
                pass
            if goOn and any(i.get('id') == int(word2find) for i in accounts):
                inAcc = True
                break
    #金额、日期、种类校验并转换:复用之前新账 种类逻辑，部分金额、日期逻辑
        elif way2find == "2" and validTime(word2find):
            word2find = validTime(word2find)
            break
        elif way2find == "3":
            goOn = validNum(word2find)
            if goOn:
                word2find = Decimal(word2find)
                word2find = str(formatAmount(word2find))
                break
        elif way2find == "4":
            if word2find in sorts:
                word2find = sorts[word2find]
                break
            elif word2find in sorts.values():
                break
        print("您再斟酌斟酌？")
        time.sleep(0.5)
    return word2find, inAcc #pyright: ignore 

#get range: s to o
def getRange(way2find, start, over):
    r = []
    if way2find == "1":
        current = int(start)
        while current <= int(over):
            r.append(current)
            current += 1
    elif way2find == "2":
        current = datetime.strptime(start, "%Y-%m-%d")#noqa DTZ007
        while current.strftime("%Y-%m-%d") <= over:
            r.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days = 1)
    elif way2find == "3":
        current = Decimal(start)
        step = Decimal('0.01')
        while current <= Decimal(over):
            r.append(current)
            current += step
    return r

#拆分并优化查账部分逻辑为方法便于复用
def findAccount(way2find, word2find, accounts):
    result = []
    for a in accounts:
        if (
                (way2find == "1" and word2find == str(a['id'])) or
                (way2find== "2" and word2find == str(a['date'])) or
                (way2find == "3" and word2find == str(a['amount'])) or
                (way2find == "4" and word2find == str(a['sort'])) or
                (way2find == "5" and word2find == str(a['mark']))
            ):
            result.append(a)
    return result

#全匹配删除，从accounts由result所有
def delAccount(result, accounts):
    accounts = [a for a in accounts if a not in result]
    return accounts

#显示账目方法（通用）
def showAccount(a,needTotal):
    print("-" * 44)
    print(f"{'ID':<8} {'日期':<10} {'类别':<4} {'金额':<8} {'备注':<8}")
    print("-" * 44)
    if not a:
        print("空空如也，记笔账吧。")
        income = expand = balance = "N/A"
    elif a and (not needTotal):
        for i in a:
            print(f"{i['id']:<4}{i['date']:<10}{i['sort']:<8}{i['amount']:<8}{i['mark']:<8}")
    else:
        income = 0
        expand = 0
        balance = 0
        for i in a:
            print(f"{i['id']:<4}{i['date']:<10}{i['sort']:<8}{i['amount']:<8}{i['mark']:<8}")
            amt = Decimal(i['amount'])
            if amt > 0:
                income += amt
            elif amt < 0:
                expand += Decimal(abs(amt))
        balance = income - expand
    print("-" * 44)
    if needTotal:
        print(f"总计:收入{income} 支出{expand} 结余{balance}")#pyright: ignore

#getgetgetget
def getSort():
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
    return sort
def getAmount():
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
    return amount
def getMark():
    mark = str(input("备注(默认”N/A“)：").strip())
    if mark == "":
        mark = "N/A"
    return mark
def getDate():
    while True:#日期
        date = str(input("日期(年-月-日，默认当天): ").strip())
        if date == "":
            date  = datetime.now().strftime("%Y-%m-%d")#noqa DTZ005
            break
        if validTime(date):
            date = validTime(date)
            break
        print("不支持的格式。")
        print("您再斟酌斟酌？")
        time.sleep(0.5)
    return date

def getValue_account():
    sort = getSort()
    amount = getAmount()
    mark = getMark()
    date = getDate()
    return sort, amount, mark, date

#ya guy really wanna change?
def changeAccount(way2change, result, accounts):
    if way2change == "5":
        sort, amount, mark, date = getValue_account()
        account = {
                        "id": result[0]["id"],
                        "sort" : sort,
                        "amount" : amount,
                        "mark" : mark,
                        "date" : date
       }
    elif way2change == "1":
        sort = getSort()
        account = {
                        "id": result[0]["id"],
                        "sort" : sort,
                        "amount" : result[0]["amount"],
                        "mark" : result[0]["mark"],
                        "date" : result[0]["date"]
        }
    elif way2change == "2":
        amount = getAmount()
        account = {
            "id": result[0]["id"],
            "sort" : result[0]["sort"],
            "amount" : amount,
            "mark" : result[0]["mark"],
            "date" : result[0]["date"]
        }
    elif way2change == "3":
        mark = getMark()
        account = {
            "id": result[0]["id"],
            "sort" : result[0]["sort"],
            "amount" : result[0]["amount"],
            "mark" : mark,
            "date" : result[0]["date"]
        }
    elif way2change == "4":
        date = getDate()
        account = {
            "id": result[0]["id"],
            "sort" : result[0]["sort"], 
            "amount" : result[0]["amount"],
            "mark" : result[0]["mark"],
            "date" : date
        }

    showAccount(account, needTotal = False)#pyright: ignore
    goOn = input("以上为改后账目,确定更改?(y)").strip()
    if goOn != "y":
        print("已取消更改。")
    delAccount(result, accounts)
    accounts.append(account)#pyright: ignore
    return accounts, goOn


__all__ = [  # noqa: RUF022
    #变量
    "iQuit", "sorts", "slections1", "slections2",
    "slections3",
    #方法
    "saveData", "loadData", "snake", "validNum",
    "formatAmount", "validTime", "checkSlection",
    "word2find_check", "getRange", "findAccount",
    "delAccount", "showAccount", "getSort", "getAmount",
    "getMark", "getDate", "getValue_account", "changeAccount",
]

