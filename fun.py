import requests
from module import sohwan

def get_id(user_name):
    api_key = 'RGAPI-caee47f0-c808-4b91-9c60-e2aeb5f61f42'

    summ = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + '?api_key=' + api_key
    r = requests.get(summ)
    new = sohwan(r.json()['id'],r.json()['accountId'],user_name)
    return new


def count_game(user_name,targetSeason):
    api_key = 'RGAPI-caee47f0-c808-4b91-9c60-e2aeb5f61f42'
    summ = get_id(user_name)

    beginIndex = 0
    endIndex = 100
    totalGame = 0
    lane_win = 0
    cham_win = 0
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

