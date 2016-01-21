import json
import random
from urllib.request import urlopen
from urllib.error import HTTPError
import os


def getownedgames(apikey, steamid):
        url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}'.format(apikey, steamid))
        #response = json.loads(urlopen(url).read().decode('utf-8'))
        response = urlopen(url).read()
        data = json.loads(response.decode('utf-8'))
        if 'response' in data.keys():
            if 'games' in data['response'].keys():
                return data['response']['games']


def getfriends(apikey,steamid):
    url = ('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend'.format(apikey,steamid))
    response = json.loads(urlopen(url).read().decode('utf-8'))
    return response['friendslist']['friends']


def getplayersname(apikey,*steamids):
    joined_string = ",".join([str(x) for x in steamids])
    url = ('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(apikey,joined_string))
    response = json.loads(urlopen(url).read().decode('utf-8'))
    player_names = []
    if 'response' in response.keys():
        if 'players' in response['response'].keys():
            for player in response['response']['players']:
                player_names.append(player["personaname"])
    return player_names

def getimage(game):
    imageurl = 'http://cdn.steampowered.com/v/gfx/apps/{}/header.jpg'
    data = urlopen(imageurl.format(game['appid'])).read()
    return ImageTk.PhotoImage(data=data)


def choosegame(games, tk, button, listbox):
    game = random.choice(games)
    try:
        game['image'] = getimage(game)
    except HTTPError:
        return choosegame(games, tk, button, listbox)

    button.configure(image=game['image'], command=lambda: playgame(game))
    friends_with_game = friends_with_same_game(apikey,getfriends(apikey,steamid),game)
    player_names = getplayersname(apikey, ",".join([player['steamid'] for player in friends_with_game]))
    listbox.delete(0, tkinter.END)
    for player_name in player_names:
        listbox.insert(tkinter.END,player_name)
    tk.title(game['name'])

def friends_with_same_game(apikey,friends, game):
    same_game_friends = []
    for friend in friends:
        friend_games = getownedgames(apikey, friend["steamid"])
        if friend_games is not None:
            for friend_game in friend_games:
                if friend_game['name'] == game['name']:
                    same_game_friends.append(friend)
    return same_game_friends


def save_steamid(steamid):
    f = open('steamids.txt','w')
    f.write(steamid + '\n')


def load_steamid(gamebutton,changebutton,listbox):
    if os.path.isfile('steamids.txt'):
        f = open('steamids.txt','r')
        steamids = f.readlines()
        text.insert(tkinter.END,steamids[0])
        gamebutton.grid(row=1,column=0)
        changebutton.invoke()
        listbox.grid(row=1,column=9)
