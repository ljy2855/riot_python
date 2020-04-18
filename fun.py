import requests
import re
import sqlite3
import time
import json

from module import sohwan


api_key = 'RGAPI-6c7b0608-1a34-43b4-ae37-4a83550e0328'
season = '13'

def get_id(user_name):

    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + '?api_key=' + api_key
    r = requests.get(url)
    new = sohwan(r.json()['id'],r.json()['accountId'],user_name)
    return new

def update_db(user_name):
    con = sqlite3.connect('./test.db')
    cur = con.cursor()
    query = "select * from USER_LIST where name = '%s';" %user_name
    print(query)
    cur.execute(query)
    summ = get_id(user_name)
    match = get_current_match(summ.accountID)
    str_match = json.dumps(match)
    
    if not cur.fetchall()   :
        cur.execute("insert into USER_LIST(name,id,accountID,update_time,match) VALUES(?,?,?,?,?);",(summ.name,summ.id,summ.accountID,int(time.time()),str_match))
    else :
        cur.execute("update USER_LIST "
        "set id = '%s', accountID = '%s', update_time = %d,match = '%s' where name = '%s';"%(summ.id,summ.accountID,int(time.time()),str_match,user_name,))

    
    con.commit()
    con.close()


#소환사 리스트 뽑기까지
def active_game(user_name):
    summ = get_id(user_name)
    print(summ.id)
    url = 'https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summ.id + '?api_key=' + api_key
    r = requests.get(url)
    print(r)
    index = 0
    new = []
    for i in r.json()['participants']:
        new.append(get_id(i['summonerName']))
        new[index].get_match_info(i['teamId'],i['championId'])
        update_db(i['summonerName'])
        print(new[index].name)
        index += 1

def all_game():
    url = 'https://kr.api.riotgames.com/lol/spectator/v4/featured-games?api_key=' + api_key
    r = requests.get(url)
    usr_list = []
    cnt = 0
    flag =1
    for i in r.json()['gameList']:
        for j in i['participants']:
            usr_list.append(j['summonerName'])
            print(j['summonerName'])
            if cnt == 100:
                flag = 0
                break
            cnt += 1
        if flag == 0:
            break        
    for i in usr_list:
        update_db(i)



#소환사 리스트 뽑기까지
def dodge():
    summ = []
    for i in range(5):
        line = input()
        index = line.find("님이 방에 참가했습니다.")
        summ.append(get_id(line[0:index]))
        update_db(summ[i].name)
        print(summ[i].name)


    

def get_current_match(accountID):
    url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountID + '?queue=420&queue=440&season=13&endIndex=50&api_key=' + api_key
    try :
        r = requests.get(url)
        match = r.json()['matches']
        return match
    except :
        print("최근 매치를 확인할수 없습니다.")






def count_game(user_name,targetSeason):
    summ = get_id(user_name)

    beginIndex = 0
    endIndex = 100
    totalGame = 0

    #'?beginIndex=' + str(beginIndex) + '?endIndex=' + str(endIndex)
    while True:
        m = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summ.accountID + '?beginIndex=' + str(beginIndex) + '&endIndex=' + str(endIndex) + '&api_key=' + api_key
        match = requests.get(m)
        print(m)
        if match.json()['startIndex'] == match.json()['endIndex'] :
            break
        if match.json()['matches'][0]['season'] == (int(targetSeason) -1) :
            break

        beginIndex = endIndex
        endIndex += 100
        totalGame += 100

    print(totalGame)

if __name__ == '__main__':
    all_game()
    


