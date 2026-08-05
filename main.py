import json
import os
import re
from datetime import datetime
import time

dataFile = "data.json"
goOn = False
sorts = {"1": "吃喝","2": "玩乐", "3": "衣", "4": "住", "5": "行", "0": "其他"}

#定义数据存取
def saveData(accounts):
    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii = False, indent = 4)
def loadData():
    if not os.path.exists(dataFile):
        return []
    with open(dataFile, "r", encoding = "utf-8") as f:
        return json.load(f)

#金额数校验
def validNum(n):
    global goOn
    expe = r'^-?\d+(\.\d{1,2})?$' #正则：整数或一/两位小数
    if re.match(expe, n):
        try:
            float(n)
            goOn = True
            return
        except ValueError:
            pass
    goOn = False
            

#时间校验
def validTime(t):
    try:
        datetime.strptime(t, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def mainMenu(): #主菜单
    accounts = loadData()
    while True:
        print("=" * 14)
        print("主菜单")
        print("=" * 14)
        print("1.新账(n)\n2.阅账(v)\n3.查账(f)\n4.划账(d)\n5.统账(c)\n6.改账(e)\n0.合账(q)")
        print("=" * 14)
        goToMenu = str(input("掌柜的，怎么说？"))


#新账
        if goToMenu == "1" or goToMenu == "n":
            print("纸笔已备好，请！")

            while True:#金额
                amount = str(input("金额: ").strip())
                validNum(amount)
                if goOn:
                    amount = float(amount)
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
                date = str(input("时间(默认当天, 格式YYYY-MM-DD): ").strip())
                if date == "":
                    date  = datetime.now().strftime("%Y-%m-%d")
                    break
                elif validTime(date):
                    break
                print("您再斟酌斟酌？")
                time.sleep(0.5)

            newID = max([r["id"] for r in accounts], default = 0) + 1#ID

            account = {
                "id" : newID,
                "sort" : sort,
                "amount" : amount,
                "mark" : mark,
                "Date" : date
            }
            
            #录入账目
            accounts.append(account)
            saveData(accounts)
            
            if len(accounts) == 1:
                print("记录是掌握生活的开始")
            print("记账成功")


        elif goToMenu == "2" or goToMenu == "v":
            pass #看
        elif goToMenu == "3" or goToMenu == "f":
            pass #查
        elif goToMenu == "4" or goToMenu == "d":
            pass #遗忘过去
        elif goToMenu == "5" or goToMenu == "c":
            pass #统计筛选
        elif goToMenu == "6" or goToMenu == "e":
            pass #更改
        elif goToMenu == "0" or goToMenu == "q":
            print("彳", end = "", flush = True)
            time.sleep(0.4)
            print("亍，", end = "", flush = True)
            saveData(accounts)
            time.sleep(0.3)
            print("那就这样吧先。")
            break #退出
        else:
            print("这不对吧，", end = "", flush = True)
            time.sleep(0.4)
            print("这对", end = "", flush = True)
            time.sleep(0.5)
            print(".", end = "", flush = True)
            time.sleep(0.5)
            print(".", end = "", flush = True)
            time.sleep(0.5)
            print(".", end = "", flush = True)
            time.sleep(0.5)
            print("吗？")
            time.sleep(0.7)

if __name__ == "__main__": mainMenu()