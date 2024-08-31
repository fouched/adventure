import game
from bestiary import monsters
from classes import Game
import config as cfg


def create_world(current_game: Game) -> (dict, int):
    # init an empty dict and a counter
    rooms: dict = {}
    monsters: int = 0

    # create room for every entry on the map
    for y in range(cfg.MAX_Y_AXIS, (cfg.MAX_Y_AXIS + 1) * -1, -1):
        for x in range(cfg.MAX_X_AXIS * -1, cfg.MAX_X_AXIS + 1):
            rm = game.generate_room(f"{x},{y}")

            if rm.monster:
                monsters = monsters + 1

            rooms[f"{x},{y}"] = rm

    return rooms, monsters

