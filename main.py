#-*- coding: utf-8 -*-
from module import sohwan
from fun import get_id, count_game


while True :
    try :
        print("1.판수 계산")
        print("2.최근 전적 분석")
        menu = input()
        if menu == '1':
            userName = input("소환사 이름 : ")
            targetSeason = input("목표 시즌 : ")
            count_game(userName,targetSeason)
        elif menu == '2':
            userName = input("소환사 이름 :")
        else:
            break
    except Exception as e:
        print(e)
        pass
