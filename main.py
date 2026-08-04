#import json
#import os
#from datetime import datetime
import time

def mainMenu(): #主菜单
    while True:
        print("=" * 14)
        print("1.新账(n)\n2.阅账(v)\n3.查账(f)\n4.划账(d)\n5.统账(c)\n6.改账(e)\n0.合账(q)")
        print("=" * 14)
        goToMenu = str(input("掌柜的，怎么说？"))
        if goToMenu == "1" or goToMenu == "n":
            pass #来新账
        elif goToMenu == "2" or goToMenu == "v":
            pass #看看
        elif goToMenu == "3" or goToMenu == "f":
            pass #查
        elif goToMenu == "4" or goToMenu == "d":
            pass #遗忘过去
        elif goToMenu == "5" or goToMenu == "c":
            pass #统计筛选
        elif goToMenu == "6" or goToMenu == "e":
            pass #更改
        elif goToMenu == "0" or goToMenu == "q":
            print("彳亍，", end = "", flush = True)
            time.sleep(0.3)
            print("那就这样吧先。")
            time.sleep(0.5)
            break #退出
        else:
            print("这不对吧，这对吗？")

if __name__ == "__main__": mainMenu()