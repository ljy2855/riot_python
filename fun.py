import requests
import re
import sqlite3
import time
import json

from module import sohwan


api_key = 'RGAPI-95ab0087-5a97-4b53-8469-a549a01ab1f5'
season = '13'

def get_id(user_name):

    try :
        url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + '?api_key=' + api_key
        r = requests.get(url)
        new = sohwan(r.json()['id'],r.json()['accountId'],user_name)
        return new
    except Exception as e:
        print(e)
def update_db(user_name):
    con = sqlite3.connect('./test.db')
    cur = con.cursor()
    for i in user_name:
    
        try :
            summ = get_id(i)
            match = get_current_match(summ.accountID)
        except Exception as e:
            print(e)
            pass
        str_match = json.dumps(match)
        score = 0
        cnt = 0
        try:
            for i in match:
                cham = i['champion']
                lane = i['lane']
                gameid = i['gameId']
                op = analy(cham,lane,gameid)
                if op != 0 :
                    cnt +=1
                    score += op
            score /= cnt
            print(score)
            query = "select * from USER_LIST where name = '{}';".format(i)
            cur.execute(query)
            time.sleep(0.5)
            if not cur.fetchall()   :
                cur.execute("insert into USER_LIST(name,id,accountID,update_time,match,score) VALUES(?,?,?,?,?,?);",(summ.name,summ.id,summ.accountID,int(time.time()),str_match,score))
            else :
                cur.execute("update USER_LIST set id = '{id}', accountID = '{aid}', update_time = {time},".format(id=summ.id,aid=summ.accountID,time=int(time.time()))\
                + "match = '{match}', score = {score} where name = '{name}';".format(match=str_match,score = score,name=summ.name))
            con.commit()
        except Exception as e:
            print(e)
            pass
    
    
    con.close()

def analy(cham,lane,gameid):
    url = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(gameid) + '?api_key=' + api_key
    r = requests.get(url)
    user = r.json()['participants']
    for i in user:
        if i['championId'] == int(cham):
            break
    if i['stats']['win'] == 1:
        score = 1
    else :
        score = -1
    
    if i['timeline']['lane'] == 'MIDDLE':
        return score
        print('mid')

    elif i['timeline']['lane'] == 'TOP':
        return score
        print('top')
    
    elif i['timeline']['lane'] == 'JUNGLE':
        return score
        print('jungle')
    elif i['timeline']['lane'] == 'BOTTOM':
        if i['timeline']['role'] == 'DUO_CARRY':
            return score
            print('ad')
        elif i['timeline']['role'] == 'DUO_SUPPORT':
            return score
            print('support')
        else :
            return 0
    else:
        return 0
        




#db 업뎃 리스트 넘겨주기 변경 필요
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
    update_db(usr_list)



#소환사 리스트 뽑기까지
def dodge():
    summ = []
    for i in range(5):
        line = input()
        index = line.find("님이 방에 참가했습니다.")
        summ.append(get_id(line[0:index]))
        analy(summ[i].name)
        print(summ[i].name)

    

    

def get_current_match(accountID):
    url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountID + '?queue=420&season=13&endIndex=10&api_key=' + api_key
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
    


