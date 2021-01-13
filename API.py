import json
from urllib.request import urlopen

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

owned_games('76561198169107517')