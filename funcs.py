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

#定义数据存取
def saveData(accs):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(accs, f, ensure_ascii = False, indent = 4)
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
    inAcc = goOn = False
    while True:
        if way == "4":
            print("可选: 1. 吃喝 2. 玩乐 3.衣 4.住 5.行 0.其他")
        word = input(q).strip()
        if (word != "0") and (word in iQuit):
            break
        elif way == "1":#by ID
            try:
                int(word)
                goOn = True
            except ValueError:
                pass
            if goOn and any(i.get('id') == int(word) for i in accs):
                inAcc = True
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
    return word, inAcc #pyright: ignore 

#get range: s to o
def getRange(way, s, o):
    r = []
    if way == "1":
        current = int(s)
        while current <= int(o):
            r.append(current)
            current += 1
    elif way == "2":
        current = datetime.strptime(s, "%Y-%m-%d")#noqa DTZ007
        while current.strftime("%Y-%m-%d") <= o:
            r.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days = 1)
    elif way == "3":
        current = Decimal(s)
        step = Decimal('0.01')
        while current <= Decimal(o):
            r.append(current)
            current += step
    return r

#拆分并优化查账部分逻辑为方法便于复用
def findAccount(way, word, accs):
    resu = []
    for a in accs:
        if (
                (way == "1" and word == str(a['id'])) or
                (way== "2" and word == str(a['date'])) or
                (way == "3" and word == str(a['amount'])) or
                (way == "4" and word == str(a['sort'])) or
                (way == "5" and word == str(a['mark']))
            ):
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

#getgetget
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

        

__all__ = [  # noqa: RUF022
    #变量
    "iQuit", "sorts", "slections1", "slections2",
    #方法
    "saveData", "loadData", "snake", "validNum",
    "formatAmount", "validTime", "checkSlection",
    "word2find_check", "getRange", "findAccount",
    "delAccount", "showAccount", "getSort", "getAmount",
    "getMark", "getDate", "getValue_account",
]
