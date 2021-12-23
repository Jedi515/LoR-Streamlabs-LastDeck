import json
import os
import re
import codecs
import datetime

ScriptName = "LoR deck"
Website = "https://www.twitch.tv/jedi515"
Creator = "Jedi515"
Version = "1.0.3"
Description = "Shows your last lor deck."

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8"
}
history_rq_line = "https://europe.api.riotgames.com/lor/match/v1/matches/by-puuid/$puuid/ids?api_key=$api_key"
last_match_line = "https://europe.api.riotgames.com/lor/match/v1/matches/{matchID}?api_key=$api_key"
request_matches_history = []
last_deck = ""
last_requested = datetime.datetime.now()

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
SETTINGS = 0


class Settings:
    def __init__(self, settings_file=None):
        with codecs.open(settings_file, encoding='utf-8-sig', mode='r') as f:
            self.__dict__ = json.load(f, encoding='utf-8-sig')


def Init():
    global SETTINGS, history_rq_line, last_match_line
    SETTINGS = Settings(settingsFile)
    history_rq_line = history_rq_line.replace("$api_key", SETTINGS.RIOT_API).replace("$puuid", SETTINGS.PUUID)
    last_match_line = last_match_line.replace("$api_key", SETTINGS.RIOT_API)
    pass


def Execute(data):
    global request_matches_history, last_deck, last_requested
    if data.IsChatMessage() and data.GetParam(0).lower() in SETTINGS.Commands:
        request_time = datetime.datetime.now()
        timediff = (request_time - last_requested).total_seconds()
        if timediff > SETTINGS.COOLDOWN:
            last_requested = request_time
            _ = json.loads(Parent.GetRequest(history_rq_line, headers)).get("response").replace('"', '').replace('[', '').replace(']', '').split(',')
            if request_matches_history != _:
                request_matches_history = _
                last_match_request = json.loads(json.loads(Parent.GetRequest(last_match_line.replace("{matchID}", _[0]), headers)).get("response"))
                for side in last_match_request.get("info").get("players"):
                    if side.get("puuid") == SETTINGS.PUUID:
                        last_deck = side.get("deck_code")

        Parent.SendStreamMessage(SETTINGS.DeckMessage.replace("$deck", last_deck).replace("$cooldown", str(int(timediff))))


def Tick():
    pass


def SendResp(data, Usage, Message):
    pass
