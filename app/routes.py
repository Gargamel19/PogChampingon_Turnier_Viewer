import json

import requests
import operator
import os

from app import app
from flask import render_template, jsonify, request
import Config


def get_games_from_dir():
    games = []
    games_path = os.path.join("data", "games")
    for file in os.listdir(games_path):
        file_path = os.path.join(games_path, file)
        with open(file_path, "r", encoding="UTF-8") as game_file:
            line = game_file.readline()
            json_game = json.loads(line.replace("'", '"'))
            json_game["ID"] = int(file_path.split(os.sep)[-1].split(". ")[0])
            games.append(json_game)
    games.sort(key=operator.itemgetter('ID'), reverse=False)
    return games


def get_game_from_dir_by_game_nr(game_nr):
    games_path = os.path.join("data", "games")
    file_path = os.path.join(games_path, game_nr + ". game.json")
    with open(file_path, "r", encoding="UTF-8") as game_file:
        line = game_file.readline()
        json_game = json.loads(line.replace("'", '"'))
        json_game["ID"] = int(file_path.split(os.sep)[-1].split(". ")[0])
        return json_game
    return None


def get_player_by_player_name(player_name):
    games_path = os.path.join("data", player_name)
    info_path = os.path.join(games_path, "infos.json")
    player = {}
    with open(info_path, "r", encoding="UTF-8") as player_file:
        player = json.loads(player_file.readline().replace("'", '"'))
    return player


@app.route("/", methods=["GET"])
def games():
    temp_games = get_games_from_dir()

    query_args = request.args
    if "liga" in query_args:
        liga = query_args["liga"]
        games_copy = []
        for game in temp_games:
            if game["liga"] == liga:
                games_copy.append(game)
        temp_games = games_copy
    if "gruppe" in query_args:
        gruppe = query_args["gruppe"]
        games_copy = []
        for game in temp_games:
            if game["gruppe"] == gruppe:
                games_copy.append(game)
        temp_games = games_copy
    print(temp_games)
    return render_template("games.html", games=temp_games)


@app.route("/player/<player_name>", methods=["GET"])
def player(player_name):
    player = get_player_by_player_name(player_name)
    return render_template("player.html", player=player)


@app.route("/game/<game_nr>", methods=["GET"])
def game(game_nr):
    temp_game = get_game_from_dir_by_game_nr(game_nr)
    player_white = get_player_by_player_name(temp_game["player_white"])
    player_black = get_player_by_player_name(temp_game["player_black"])
    return render_template("game.html", game=temp_game, player_white=player_white, player_black=player_black)
