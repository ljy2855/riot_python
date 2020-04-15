import requests
import re
from module import sohwan

api_key = 'RGAPI-02d294e0-16b8-4e0f-9920-7bd3da3ea8e0'

def get_id(user_name):

    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + '?api_key=' + api_key
    r = requests.get(url)
    new = sohwan(r.json()['id'],r.json()['accountId'],user_name)
    return new


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
        get_current_match(new[index],20)
        index += 1

def dodge():
    summ = []
    for i in range(5):
        line = input()
        index = line.find("님")
        summ.append(get_id(line[0:index]))
        get_current_match(summ[i],30)


    
    
def get_current_match(sohwan,cnt):
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

