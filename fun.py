import requests
import re
import sqlite3
from module import sohwan


api_key = 'RGAPI-02d294e0-16b8-4e0f-9920-7bd3da3ea8e0'

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
    if not cur.fetchall()   :
        cur.execute("insert into USER_LIST(name,id,accountID) VALUES(?,?,?);",(summ.name,summ.id,summ.accountID))
    
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

#소환사 리스트 뽑기까지
def dodge():
    summ = []
    for i in range(5):
        line = input()
        index = line.find("님")
        summ.append(get_id(line[0:index]))
        get_current_match(summ[i])


    

def get_current_match(sohwan):
    url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + sohwan.accountID + '&api_key=' + api_key
    r = requests.get(url)






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

