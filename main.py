# SPDX-FileCopyrightText: 2026 Annaler
# SPDX-License-Identifier: MPL-2.0
#pylint:disable=W0614, W0401
import time
from decimal import Decimal

from funcs import *


def mainMenu():#主菜单
    accounts = loadData()
    while True:
        print("=" * 44)
        print("钱都去哪了?")
        print("=" * 44)
        print("1.新账(n) 2.阅账(v) 3.查账(f)\n4.划账(d) 5.统账(c) 6.改账(e)\n0.合账(q)")
        print("=" * 44)
        go2menu = str(input("掌柜的，怎么说？"))

#新账
        if go2menu == "1" or go2menu == "n":
            while True:
                print("纸笔已备好，请！")

                newID = max([r["id"] for r in accounts], default = 0) + 1#ID

                sort, amount, mark, date = getValue_account()

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
                    goOn = input("再记一笔？(y)")
                    if goOn == "y":
                        continue
                    else:
                        goOn = True
                        break
                if goOn:
                    break

#阅账 Issue:账目格式/排版
        elif go2menu == "2" or go2menu == "v":
            showAccount(accounts, needTotal = True)
            while True:
                back = input("回到主菜单？(y)")
                if back == "y":
                    break

#查账
        elif go2menu == "3" or go2menu == "f":
            while True:
                way2find = ""
                while True:
                    print("-" * 19, "查账", "-" * 19)
                    print("以何为规？")
                    print("可选：1. ID(i) 2. 日期(d) 3. 金额(a)\n4.类别(s) 5. 备注(m) 0.退出(q)" ) 
                    way2find = input("您的选择？").strip()
                    if way2find in iQuit:
                        break 
                    way2find, goOn = checkSlection(way2find, slections1)
                    if goOn == False:
                        print("目前只支持以上选项哦。")
                        continue

                    quiz = "用于查询的关键词："
                    while True:
                        word2find, inAccs = word2find_check(way2find, quiz, accounts)
                        if ( way2find != "1" ) and inAccs:
                            break
                        print("您再斟酌斟酌？")

                    result = findAccount(way2find, word2find, accounts)
                    if len(result) == 0:
                        snake()
                    else:
                        print(f"共找到{len(result)}条账目，立刻供上。")
                        time.sleep(0.5)
                        showAccount(result, needTotal = True)

                if way2find not in iQuit:
                    goOn = input("还查账吗？(y)")
                    if goOn != "y":
                        break

#划账
        elif go2menu == "4" or go2menu == "d":
            while True:
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
                    way2find, goOn = checkSlection(way2find, slections1)
                    if goOn == False:
                        print("目前只支持以上选项哦。")
                        continue

                    quiz = "用于划账的关键词："
                    while True:
                        word2find, inAccs = word2find_check(way2find, quiz, accounts)
                        if inAccs:
                            break
                        print("您再斟酌斟酌？")
                        time.sleep(0.2)
                    if inAccs:
                        break
                    #issue:如果用户在word2find想退出(到上一步?)。考虑iQuit

        #加入先让人过一眼要删除的y/n再删除
                    result = findAccount(way2find, word2find, accounts)
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
                            showAccount(result, needTotal = False)
                            if input("确认要划账吗(y)？").strip() != "y":
                                break
                        accounts = delAccount(result, accounts)
                    saveData(accounts)
                    loadData()

                if way2find not in iQuit:
                    time.sleep(0.2)
                    goOn = input("再划？(y)")
                    if goOn != "y":
                        break

#统计筛选
        elif go2menu == "5" or go2menu == "c":
            while True:
                while True:
                    needCheck = True
                    equal = False
                    print("-" * 19, "划账", "-" * 19)
                    print("按啥统账？")
                    print("可选：1. ID(i) 2. 日期(d) 3. 金额(a)\n4.类别(s) 0.退出(q)")
                    way2find = input("您说呢？")
                    if way2find in iQuit:
                        break
                    way2find, goOn = checkSlection(way2find, slections2) 
                    if not goOn:
                        continue
                    elif way2find == "4":
                        needCheck = False
                        quiz = "用于统计的关键词："
                        word2find, _ = word2find_check(way2find, quiz, accounts)
                    
                    while needCheck:
                        quiz = "这总得开个头吧："
                        start, _ = word2find_check(way2find, quiz, accounts)
                        quiz = "这总得结个尾吧："
                        over, _ = word2find_check(way2find, quiz, accounts)
                        #start比大小over
                        if start == over:
                            equal = True
                        elif (
                                (( way2find == "1" ) and ( int(start) < int(over) )) or
                                (( way2find == "2" ) and ( start < over )) or#pyright: ignore
                                (( way2find == "3" ) and ( Decimal(start) < Decimal(over) ))
                              ):
                            break
                        print("还请您再斟酌斟酌")
                        time.sleep(0.1)

                    result = []
                    if (not equal) and needCheck: 
                        rangeList = getRange(way2find, start, over)#pyright: ignore
                        #word2find = 1 =2 =3从start到over(这段定义为rang).append到result
                        for w in rangeList:
                            result.extend(findAccount(way2find, w, accounts))
                    elif equal and needCheck:
                        word2find = start#pyright: ignore
                        result = findAccount(way2find, word2find, accounts)
                    else: 
                        result = findAccount(way2find, word2find, accounts)# pyright: ignore
                    showAccount(result, needTotal = True)

                if way2find not in iQuit:
                    time.sleep(0.2)
                    goON = input("还统么？(y)")
                    if goON != "y":
                        break

#改账
        elif go2menu == "6" or go2menu == "e":
            while True:
                print("-" * 19, "改账", "-" * 19)
                while True:#getID
                    quiz = "请输入目标账目ID:"
                    targetID, inAccs = word2find_check("1", quiz, accounts)
                    if targetID in iQuit:
                        break
                    if inAccs:
                        break
                if targetID in iQuit:
                    break
                result = findAccount("1", targetID, accounts)
                showAccount(result, needTotal = False)
            #getWay
                while True:
                    print("-" * 44)
                    print("掌柜的，改甚？")
                    print("可选: 1. 种类(s) 2. 金额(a) 3. 备注(m) 4. 日期(d) 5. 重写(r) 0.退出(q)")
                    way2change = input("怎么改？")
                    if way2change in iQuit:
                        break
                    way2change, goOn = checkSlection(way2change, slections3)
                    if not goOn:
                        print("目前仅支持以上选项。")
                    else:
                        break
                if way2change in iQuit:
                    break
            #change account
                accounts, goOn = changeAccount(way2change, result, accounts)
                if goOn == "y":
                    saveData(accounts)
                    loadData()
                    print("改账成功。", end = "", flush = True)
                    time.sleep(0.2)

                goOn = input("再改一笔？(y)").strip()
                if goOn != "y":
                    break

#合账-退出
        elif go2menu in iQuit:
            print("彳", end = "", flush = True)
            time.sleep(0.4)
            print("亍，", end = "", flush = True)
            time.sleep(0.3)
            print("那就这样吧先。")

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
