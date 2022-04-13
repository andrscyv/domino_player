import datetime
import sqlite3
import json
from typing import Set

from simulation_utils import PlayRecord


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def extract_pips(tile):
    if not tile:
        return (None, None)

    tile_as_list = list(tile)
    if len(tile_as_list) == 0:
        return (None, None)

    if len(tile_as_list) == 1:
        return (tile_as_list[0], tile_as_list[0])

    if len(tile_as_list) == 2:
        return (tile_as_list[0], tile_as_list[1])


def extract_suits(suits_at_end: Set[int]):
    if not suits_at_end:
        return (None, None)

    suits_at_end = list(suits_at_end)

    if len(suits_at_end) == 0:
        return (None, None)

    if len(suits_at_end) == 1:
        return (suits_at_end[0], suits_at_end[0])

    if len(suits_at_end) == 2:
        return (suits_at_end[0], suits_at_end[1])


class Recorder:
    def __init__(self, conn_name, num_games):
        self.conn = sqlite3.connect(conn_name)
        c = self.conn.cursor()
        c.execute(
            (
                "CREATE TABLE IF NOT EXISTS experiment("
                "experiment_id INTEGER PRIMARY KEY,"
                "num_games INTEGER"
                ") "
            )
        )
        c.execute(
            (
                "CREATE TABLE IF NOT EXISTS game("
                "game_id INTEGER PRIMARY KEY,"
                "experiment_id INTEGER,"
                "creation_date TEXT,"
                "p1 TEXT,"
                "p2 TEXT,"
                "p3 TEXT,"
                "p4 TEXT,"
                "first_player TEXT,"
                "p1_tiles TEXT,"
                "p2_tiles TEXT,"
                "p3_tiles TEXT,"
                "p4_tiles TEXT,"
                "winner INTEGER,"
                "FOREIGN KEY(experiment_id) REFERENCES experiment(experiment_id)"
                ") "
            )
        )
        c.execute(
            (
                "CREATE TABLE IF NOT EXISTS play("
                "game_id INTEGER NOT NULL,"
                "player TEXT,"
                "player_number INTEGER,"
                "pip1 INTEGER,"
                "pip2 INTEGER,"
                "suit_at_end_l INTEGER,"
                "suit_at_end_r INTEGER,"
                "p1_tiles TEXT,"
                "p2_tiles TEXT,"
                "p3_tiles TEXT,"
                "p4_tiles TEXT,"
                "play_number INTEGER,"
                "suit_played INTEGER,"
                "FOREIGN KEY (game_id) REFERENCES game(game_id)"
                ") "
            )
        )
        self.conn.commit()
        self.experiment_id = self.create_new_experiment_record(num_games)

    def create_new_experiment_record(self, num_games) -> int:
        c = self.conn.cursor()
        c.execute(
            ("INSERT INTO experiment(num_games) VALUES(?)"),
            (num_games,),
        )
        experiment_id = c.lastrowid
        self.conn.commit()
        return experiment_id

    def create_new_game_record(self, players, first_player, tiles) -> int:
        c = self.conn.cursor()
        c.execute(
            (
                "INSERT INTO game ("
                "experiment_id,"
                "creation_date,"
                "p1,"
                "p2,"
                "p3,"
                "p4,"
                "first_player,"
                "p1_tiles,"
                "p2_tiles,"
                "p3_tiles,"
                "p4_tiles"
                ")"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                self.experiment_id,
                str(datetime.datetime.now()),
                players[0],
                players[1],
                players[2],
                players[3],
                first_player,
                json.dumps(tiles[0], cls=SetEncoder),
                json.dumps(tiles[1], cls=SetEncoder),
                json.dumps(tiles[2], cls=SetEncoder),
                json.dumps(tiles[3], cls=SetEncoder),
            ),
        )
        game_id = c.lastrowid
        self.conn.commit()
        return game_id

    def save_winner(self, game_id, winner):
        c = self.conn.cursor()
        c.execute(
            ("UPDATE game SET winner = ? WHERE game_id = ?"),
            (winner, game_id),
        )
        self.conn.commit()

    def save_record_list(self, game_id: int, play_record_list: list[PlayRecord]):
        c = self.conn.cursor()

        for idx, play_record in enumerate(play_record_list):
            state = play_record.state
            suit_played = None
            pip1 = None
            pip2 = None
            suit_l = None
            suit_r = None
            if state.action:
                tile = state.action.tile
                suit_played = state.action.suit_played
                pip1, pip2 = extract_pips(tile)
                suit_l, suit_r = extract_suits(state._suits_at_ends)
            c.execute(
                (
                    "INSERT INTO play ("
                    "game_id,"
                    "player,"
                    "player_number,"
                    "pip1,"
                    "pip2,"
                    "suit_at_end_l,"
                    "suit_at_end_r,"
                    "suit_played,"
                    "p1_tiles,"
                    "p2_tiles,"
                    "p3_tiles,"
                    "p4_tiles,"
                    "play_number"
                    ")"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                ),
                (
                    game_id,
                    play_record.player_string,
                    play_record.player_number + 1,
                    pip1,
                    pip2,
                    suit_l,
                    suit_r,
                    suit_played,
                    json.dumps(state._tiles_by_player[0], cls=SetEncoder),
                    json.dumps(state._tiles_by_player[1], cls=SetEncoder),
                    json.dumps(state._tiles_by_player[2], cls=SetEncoder),
                    json.dumps(state._tiles_by_player[3], cls=SetEncoder),
                    idx,
                ),
            )
            self.conn.commit()

    def close(self):
        self.conn.close()
