import click
import os
import csv
from flask.cli import with_appcontext


@click.command(name='create_files')
@with_appcontext
def create_files():
    excludes = [
        "3te Gruppe A",
        "2te Gruppe A",
        "1te Gruppe A",
        "3te Gruppe B",
        "2te Gruppe B",
        "1te Gruppe B",
        "Verlierer Duell 1",
        "Verlierer Duell 2",
        "Gewinner Duell 1",
        "Gewinner Duell 2",
    ]
    from app import app

    games_dir = "data/games"
    if not os.path.exists(games_dir):
        os.makedirs(games_dir)

    with open("data/plan.csv", "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        index = 0
        for row in spamreader:
            if not index == 0:

                name_player_1 = row[7]
                name_player_2 = row[14]

                game_data = {
                    "player_white": name_player_1,
                    "player_black": name_player_2,
                    "date": row[2],
                    "time": row[0],
                    "phase": row[4],
                    "liga": row[5],
                    "gruppe": row[6],
                }

                with open(os.path.join(games_dir, str(index) + ". game.json"), "w+") as info_file:
                    info_file.writelines(str(game_data))

                liga = row[5]
                gruppe = row[6]
                if row[7] not in excludes:
                    elo_player_1 = row[10]
                    lichess_player_1 = None
                    if row[11]:
                        lichess_player_1 = "https://lichess.org/@/" + row[11].split(": ")[1]
                    chesscom_player_1 = None
                    if row[12]:
                        chesscom_player_1 = "https://www.chess.com/member/" + row[12].split(": ")[1]
                    beschreibung_player_1 = row[13]
                    directory = "data/{}".format(name_player_1)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        player = {
                            "liga": liga,
                            "gruppe": gruppe,
                            "name": name_player_1,
                            "elo": elo_player_1,
                            "beschreibung": beschreibung_player_1
                        }
                        if lichess_player_1:
                            player["lichess"] = lichess_player_1
                        if chesscom_player_1:
                            player["chesscom"] = chesscom_player_1
                        with open(os.path.join(directory, "infos.json"), "w+") as info_file:
                            info_file.writelines(str(player))
                if row[14] not in excludes:
                    elo_player_2 = row[17]
                    lichess_player_2 = None
                    if row[18]:
                        lichess_player_2 = "https://lichess.org/@/" + row[18].split(": ")[1]
                    chesscom_player_2 = None
                    if row[19]:
                        chesscom_player_2 = "https://www.chess.com/member/" + row[19].split(": ")[1]
                    beschreibung_player_2 = row[20]
                    directory = "data/{}".format(name_player_2)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        player = {
                            "liga": liga,
                            "gruppe": gruppe,
                            "name": name_player_2,
                            "elo": elo_player_2,
                            "beschreibung": beschreibung_player_2
                        }
                        if lichess_player_2:
                            player["lichess"] = lichess_player_2
                        if chesscom_player_2:
                            player["chesscom"] = chesscom_player_2
                        with open(os.path.join(directory, "infos.json"), "w+") as info_file:
                            info_file.writelines(str(player))
                print(row[5], ":", row[7], "vs.", row[14])
            index = index + 1
