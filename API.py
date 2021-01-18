import json
from urllib.request import urlopen
import time

# steam id = 76561198169107517
# api code = 0303DC2418211FDE854C25DB323816C2

def totale_gametijd(steam_id):
    url_games = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=0303DC2418211FDE854C25DB323816C2&steamid=' + steam_id + '&format=json'
    with urlopen(url_games) as response:
        source = response.read()
    games = json.loads(source)
    totaal = 0
    for game_data in games['response']['games']:
        totaal = totaal + int(game_data['playtime_forever'])
    return round((totaal / 60), 2)


def naam(steam_id):
    url_gebruikers_info = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=0303DC2418211FDE854C25DB323816C2&steamids=' + steam_id
    with urlopen(url_gebruikers_info) as response:
        source = response.read()
    gebruikers_info = json.loads(source)
    return gebruikers_info['response']['players'][0]['personaname']


def owned_games(steam_id):
    url_games = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=0303DC2418211FDE854C25DB323816C2&steamid=' + steam_id + '&include_appinfo=True&format=json'
    with urlopen(url_games) as response:
        source = response.read()
    games = json.loads(source)
    string = ''
    for game in games['response']['games']:
        string = string + game['name'] + '\n'
    return string


def vrienden_online(steam_id):
    url_games = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=0303DC2418211FDE854C25DB323816C2&steamid=' + steam_id + '&relationship=friend'
    with urlopen(url_games) as response:
        source = response.read()
    vrienden_lijst = json.loads(source)
    vrienden_ids = []
    for info_vriend in vrienden_lijst['friendslist']['friends']:
        vrienden_ids.append(info_vriend['steamid'])
    vrienden_status = []
    for id in vrienden_ids:
        url_games = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=0303DC2418211FDE854C25DB323816C2&steamids=' + id
        with urlopen(url_games) as response:
            source = response.read()
        vriend = json.loads(source)
        vrienden_status.append([vriend['response']['players'][0]['personaname'], vriend['response']['players'][0]['personastate']])
    return vrienden_status


def recently_played(steam_id):
    url_games = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=0303DC2418211FDE854C25DB323816C2&steamid=' + steam_id + '&format=json'
    with urlopen(url_games) as response:
        source = response.read()
    info = json.loads(source)
    aantal_games = info["response"]["total_count"]
    games = []
    for game in info["response"]["games"]:
        games.append(game["name"])
    return [aantal_games, games]


def account_aangemaakt(steam_id):
    url_gebruikers_info = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=0303DC2418211FDE854C25DB323816C2&steamids=' + steam_id
    with urlopen(url_gebruikers_info) as response:
        source = response.read()
    gebruikers_info = json.loads(source)
    return time.gmtime(gebruikers_info["response"]["players"][0]["timecreated"])


# print(account_aangemaakt('76561198169107517'))