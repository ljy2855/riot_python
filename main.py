#-*- coding: utf-8 -*-
from module import sohwan
from fun import get_id, count_game, active_game, dodge, update_db, analy



while True :
    try :
        print("1.판수 계산")
        print("2.최근 전적 분석")
        print("3.진행중인 게임")
        print("4.소환사 id 확인")
        print("5.닷지할끼?")
        print("6.db 업뎃")
        menu = input()
        if menu == '1':
            userName = input("소환사 이름 : ")
            targetSeason = input("목표 시즌 : ")
            count_game(userName,targetSeason)
        elif menu == '2':
            userName = input("소환사 이름 :")
            analy(userName)
        elif menu == '3':
            userName = input("소환사 이름: ")
            active_game(userName)
        elif menu == '4':
            userName = input("소환사 이름 : ")
            print(get_id(userName).id,get_id(userName).accountID)
        elif menu == '5':
            dodge()
        elif menu == '6':
            userName = input("소환사 이름: ")
            usr_list =[]
            usr_list.append(userName)
            update_db(usr_list)



        else:
            break
    except Exception as e:
        print(e)
        pass
