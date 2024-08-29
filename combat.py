import random

from random import randint
from time import sleep

from colorama import Fore

from classes import Game
from util import get_yn
import config as cfg


def fight(current_game: Game) -> str:
    rm = current_game.room
    player = current_game.player

    players_turn = True
    # flip a coin for 1st turn
    if random.randint(1,2) == 2:
        players_turn = False

    if players_turn:
        print(f"{Fore.CYAN}You brace yourself and attack the {rm.monster['name']}.")
    else:
        print(f"The {rm.monster['name']} moves quickly and attacks first!")

    # get monster's hit points
    monster_hp = random.randint(rm.monster["min_hp"], rm.monster["max_hp"])
    monster_original_hp = monster_hp

    # TODO: adjust attack rolls for player and monster
    winner = ""
    while True:
        if players_turn:
            my_roll = random.randint(1, 100)

            # 50% change to hit
            if my_roll > 50:
                print(f"{Fore.GREEN}You hit the {rm.monster['name']} with your {player.current_weapon['name']}!")
                monster_hp = monster_hp - randint(player.current_weapon['min_damage'],
                                                  player.current_weapon['max_damage'])
            else:
                print(f"{Fore.GREEN}You attack the {rm.monster['name']} with your {player.current_weapon['name']} and miss!")

            if monster_hp <= 0:
                print(f"{Fore.GREEN}The {rm.monster['name']} falls to the floor, dead.")
                winner = "player"
        else:
            # monster's turn
            monster_roll = random.randint(1, 100)

            if monster_roll > 50:
                print(f"{Fore.RED}The {rm.monster['name']} attacks and hits!")
                player.hp = player.hp - random.randint(rm.monster['min_damage'], rm.monster['max_damage'])
            else:
                print(f"{Fore.GREEN}The {rm.monster['name']} attacks and misses!")

            if player.hp <= 0:
                print(f"{Fore.RED}The {rm.monster['name']} kills you, and you fall to the floor, dead.")
                winner = "monster"


        if player.hp <= 0 or monster_hp <= 0:
            break

        if player.hp <= int(0.2 * cfg.PLAYER_HP):
            answer = get_yn("You are near death. Do you want to continue")
            if answer == "no":
                return "flee"
        elif player.hp <= int(0.4 * cfg.PLAYER_HP):
            answer = get_yn("You are badly wounded. Do you want to continue")
            if answer == "no":
                return "flee"
        elif player.hp <= int(0.6 * cfg.PLAYER_HP):
            answer = get_yn("You are wounded. Do you want to continue")
            if answer == "no":
                return "flee"
        elif player.hp <= cfg.PLAYER_HP:
            print("You are only lightly wounded. 'Tis but a scratch.")

        sleep(1)
        print("")

        players_turn = not players_turn


    return winner

