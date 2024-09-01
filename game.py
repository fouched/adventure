import random
from traceback import print_tb

import armory
import bestiary
import combat
import config as cfg
import world
from classes import Player, Room, Game
from util import get_yn


from colorama import Fore, Back, init




def welcome(current_game: Game):

    print(Fore.RED + "                                                  D U N G E O N")
    print(Fore.GREEN + """
    The village of Honeywood has been terrorized by strange, deadly creatures for months now. Unable to endure any 
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with nothing but a bundle of torches, you descend into the labyrinth, 
    ready to do battle....""")

    print()
    print(f"According the the people of Honeywood there are {current_game.num_monsters} creatures in this labyrinth.")
    print()


def play_game(term):

    # init makes sure that colorama works on various platforms
    init()

    adventurer = Player()

    current_game = Game(adventurer, cfg.MAX_X_AXIS, cfg.MAX_Y_AXIS, term)

    all_rooms, num_monsters = world.create_world(current_game)
    current_game.num_monsters = num_monsters
    current_game.set_rooms(all_rooms)

    entrance = "0,0"
    current_game.set_current_room(current_game.rooms[entrance])
    current_game.set_entrance(entrance)
    current_game.room.location = entrance

    # draw top status bar
    draw_ui(current_game)

    welcome(current_game)

    # get player input
    input(f"{Fore.CYAN}Press enter to begin...")
    current_game.room.print_description()
    explore_labyrinth(current_game)


# generate room
def generate_room(location: str) -> Room:

    items = []
    monster = {}

    # there is a 25% chance that this room has an item
    if random.randint(1, 100) < 26:
        i = random.choice(list(armory.items.values()))
        items.append(i)

    # there is a 25% chance that this room has monster
    if random.randint(1, 100) < 26:
        monster = random.choice(bestiary.monsters)


    return Room(items, monster, location)


def explore_labyrinth(current_game: Game):

    while True:

        for i in current_game.room.items:
            print(f"{Fore.YELLOW}You see a {i['name']}.")

        if current_game.room.monster:
            print(f"{Fore.RED}There is a {current_game.room.monster['name']} here!")
            # draw top status bar
            draw_ui(current_game)
            fight_or_flee = get_input("Do you want to fight or flee?", ["fight", "flee"])

            while True:
                if fight_or_flee == "flee":
                    print(f"{Fore.CYAN}You turn and run, coward that you are...")
                    # draw top status bar
                    draw_ui(current_game)
                    break
                else:
                    winner = combat.fight(current_game)
                    if winner == "player":
                        gold = random.randint(1, 100)
                        print(f"You search the monster's body and find {gold} pieces of gold.")
                        current_game.player.treasure = current_game.player.treasure + gold
                        current_game.player.xp = current_game.player.xp + 100
                        current_game.player.monsters_defeated = current_game.player.monsters_defeated + 1
                        current_game.room.monster = {}
                        # draw top status bar
                        draw_ui(current_game)
                        break
                    elif winner == "monster":
                        print(f"{Fore.RED}You have failed in your mission, and your body lies in the labyrinth forever.")
                        # draw top status bar
                        draw_ui(current_game)
                        play_again()
                        break
                    else:
                        print(f"{Fore.CYAN}You flee in terror from the monster.")
                        # draw top status bar
                        draw_ui(current_game)
                        break

        # draw top status bar
        draw_ui(current_game)

        player_input = input(f"{Fore.YELLOW}-> {Fore.WHITE}").lower().strip()

        # process input
        if player_input == "help":
            show_help()
            continue

        elif player_input == "look":
            current_game.room.print_description()
            continue

        elif player_input == "map":
            show_map(current_game)
            continue

        elif player_input.startswith("get"):
            if not current_game.room.items:
                print(f"{Fore.CYAN}There is nothing to pick up.")
                continue
            else:
                get_an_item(current_game, player_input)
                continue

        elif player_input == "inventory" or player_input == "inv":
            show_inventory(current_game)
            continue

        elif player_input.startswith("drop"):
            drop_an_item(current_game, player_input)
            continue

        elif player_input.startswith("equip"):
            use_item(current_game.player, player_input[6:])
            continue

        elif player_input.startswith("use"):
            use_item(current_game.player, player_input[4:])
            continue

        elif player_input.startswith("unequip"):
            unequip_item(current_game.player, player_input[8:])
            continue

        elif player_input == "rest" or player_input == "r":
            rest(current_game)
            continue

        elif player_input in ["n", "s", "e", "w"]:
            direction = player_input
            if current_game.room.location == current_game.entrance and direction == "s":
                yn = get_yn(f"{Fore.CYAN}You are about to leave the dungeon, are you sure")
                if yn == "yes":
                    play_again()
                else:
                    continue


            if direction == "n":
                if current_game.player.y_coord < current_game.y:
                    current_game.player.y_coord = current_game.player.y_coord + 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "s":
                if current_game.player.y_coord > (current_game.y * -1):
                    current_game.player.y_coord = current_game.player.y_coord - 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "e":
                if current_game.player.x_coord < current_game.x:
                    current_game.player.x_coord = current_game.player.x_coord + 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "w":
                if current_game.player.x_coord > (current_game.x * -1):
                    current_game.player.x_coord = current_game.player.x_coord - 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            print(f"{Fore.CYAN}You move deeper into the dungeon.")

            # draw top status bar
            draw_ui(current_game)

        elif player_input == "status":
            print_status(current_game)
            continue

        elif player_input == "q" or player_input == "quit":
            print(f"{Fore.YELLOW}Overcome with terror, you flee the dungeon.")
            # TODO: print out final score
            play_again()

        else:
            print(f"{Fore.CYAN}I'm not sure what you mean... type help for available commands.")
            continue

        new_location = f"{current_game.player.x_coord},{current_game.player.y_coord}"
        current_game.room = current_game.rooms[new_location]
        current_game.room.location = new_location

        if new_location in current_game.player.visited:
            print(f"{Fore.YELLOW}This place seems familiar...")
        else:
            current_game.player.visited.append(new_location)

        current_game.room.print_description()
        current_game.player.turns += 1


def rest(current_game: Game):
    if current_game.player.hp == cfg.PLAYER_HP:
        print(f"{Fore.CYAN}You are fully rested, and feel great. There is no point in sitting around...")
    else:
        current_game.player.hp = current_game.player.hp + random.randint(1, 10)
        if current_game.player.hp > cfg.PLAYER_HP:
            current_game.player.hp = cfg.PLAYER_HP

        print(f"{Fore.CYAN}You feel better ({current_game.player.hp}/{cfg.PLAYER_HP} hit points).")


def show_map(current_game: Game):
    #print the top line
    for i in range(1, cfg.MAX_X_AXIS * 6 + 3):
        print(Fore.YELLOW + "-", end="")
    print()

    for y in range(cfg.MAX_Y_AXIS, (cfg.MAX_Y_AXIS + 1) * -1, -1):
        for x in range(cfg.MAX_X_AXIS * -1, cfg.MAX_X_AXIS + 1):
            content = ""
            if f"{x},{y}" == current_game.room.location:
                # our current location
                content = Fore.RED + Back.WHITE + " X " + Fore.YELLOW + Back.RESET
            elif f"{x},{y}" == current_game.entrance:
                content = Fore.GREEN + Back.WHITE + " E " + Fore.YELLOW + Back.RESET
            elif f"{x},{y}" in current_game.player.visited:
                # a place we've visited
                test_room = current_game.rooms[f"{x},{y}"]
                if test_room.monster:
                    # we left a monster in this room
                    content = Fore.RED + " M " + Fore.YELLOW
                else:
                    pass
            else:
                content = " ? "

            print(Fore.YELLOW + f"{content.center(3)}", end="")

        print()

    # print the bottom line
    for i in range(1, cfg.MAX_X_AXIS * 6 + 3):
        print(Fore.YELLOW + "-", end="")
    print()
    #print the legend
    print(Back.WHITE + Fore.RED + " X " + Back.RESET + ": You  ", end="")
    print(Fore.RED + " M " + Back.RESET + ": Monster  ", end="")
    print(Back.WHITE + Fore.GREEN + " E " + Back.RESET + ": Exit")



def print_status(current_game: Game):
    print(Fore.CYAN)
    print(f"You have played the game for {current_game.player.turns} turns, "
          + f"defeated {current_game.player.monsters_defeated} monsters, "
          + f"and found {current_game.player.treasure} gold pieces.")
    print(f"You have earned {current_game.player.xp} xp.")
    print(f"You have {current_game.player.hp} hit points remaining, out of 100.")
    print(f"Currently equipped weapon: {current_game.player.current_weapon['name']}")
    print(f"Currently equipped armor: {current_game.player.current_armor['name']}")
    print(f"Currently equipped shield: {current_game.player.current_shield['name']}")


def unequip_item(player: Player, item:str):

    if item in player.inventory:
        if player.current_weapon["name"] == item:
            player.current_weapon = armory.default["hands"]
            print(f"{Fore.CYAN}You stop using the {item}.")
        elif player.current_armor["name"] == item:
            player.current_armor = armory.default["clothes"]
            print(f"{Fore.CYAN}You stop using the {item}.")
        elif player.current_shield["name"] == item:
            player.current_shield = armory.default["no shield"]
            print(f"{Fore.CYAN}You stop using the {item}.")
        else:
            print(f"{Fore.RED}You don't have a {item} equipped!")
    else:
        print(f"{Fore.RED}You don't have a {item}.")



def use_item(player: Player, item: str):

    if item in player.inventory:
        old_weapon = player.current_weapon

        if armory.items[item]["type"] == "weapon":
            player.current_weapon = armory.items[item]
            print(f"{Fore.CYAN}You arm yourself with a {player.current_weapon['name']} "
                    + f"instead of your {old_weapon['name']}.")

            # you can't use a shield with a bow
            if item == "longbow" and player.current_shield["name"] != "no shield":
                player.current_shield = armory.default["no shield"]
                print(f"{Fore.CYAN}Since you can't use a shield with a {item}, you sling it over your back.")

        elif armory.items[item]["type"] == "armor":
            player.current_armor = armory.items[item]
            print(f"{Fore.CYAN}You put on the {player.current_armor['name']}.")
        elif armory.items[item]["type"] == "shield":
            # you can't use a shield with a bow
            if player.current_weapon['name'] == "longbow":
                print(f"{Fore.RED}You can't use a shield while you are using a bow.")
            else:
                player.current_shield = armory.items[item]
                print(f"{Fore.CYAN}You equip your {player.current_shield['name']}.")
        else:
            print(f"{Fore.RED}You can't equip a {item}.")
    else:
        print(f"{Fore.RED}You don't have a {item}.")



def drop_an_item(current_game: Game, player_input: str):

    if player_input[5:] == current_game.player.current_weapon["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped weapon!")
    elif player_input[5:] == current_game.player.current_armor["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped armor!")
    elif player_input[5:] == current_game.player.current_shield["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped shield!")
    else:
        try:
            current_game.player.inventory.remove(player_input[5:])
            print(f"{Fore.CYAN}You drop the {player_input[5:]}.")
            current_game.room.items.append(armory.items[player_input[5:]])
        except ValueError:
            print(f"{Fore.RED}You are not carrying a {player_input[5:]}!")


def show_inventory(current_game: Game):

    print(f"{Fore.CYAN}Your inventory:")
    print(f"    - {current_game.player.treasure} pieces of gold.")

    for x in current_game.player.inventory:
        if x == current_game.player.current_weapon["name"]:
            print(f"    - {x.capitalize()} (equipped)")
        elif x == current_game.player.current_armor["name"]:
            print(f"    - {x.capitalize()} (equipped)")
        elif x == current_game.player.current_shield["name"]:
            print(f"    - {x.capitalize()} (equipped)")
        else:
            print(f"    - {x.capitalize()}")



def get_an_item(current_game: Game, player_input: str):

    if len(current_game.room.items) > 0 and player_input[4:] == "":
        player_input = player_input + " " + current_game.room.items[0]["name"]

    if player_input[4:] not in current_game.player.inventory:
        idx = find_in_list(player_input[4:], "name", current_game.room.items)

        if idx > -1:
            cur_item = current_game.room.items[idx]
            current_game.player.inventory.append(cur_item["name"])
            current_game.room.items.pop(idx)
            print(f"{Fore.CYAN}You pick up the {cur_item['name']}.")
        else:
            print(f"{Fore.RED}There is no {player_input[4:]}here.")
    else:
        print(f"{Fore.CYAN}You already have a {player_input[4:]}, and decide you don't need another one.")


def find_in_list(search_string: str, key: str, list_to_search: list) -> int:

    idx = -1
    count = 0
    for item in list_to_search:
        if item[key] == search_string:
            idx = count
        count += 1

    return idx


def play_again():

    yn = get_yn(Fore.CYAN + "Play again")
    if yn == "yes":
        play_game()
    else:
        print(f"{Fore.YELLOW}Until next time, adventurer.")
        exit(0)


# get_input prompts the user for input, and limits responses to whatever is in the list of answers
def get_input(question: str, answers:list) -> str:
    while True:
        resp = input(f"{Fore.CYAN}{question} {Fore.YELLOW}-> {Fore.WHITE}").lower().strip()
        if resp not in answers:
            print(f"{Fore.YELLOW}Please enter a valid response.")
        else:
            return resp


def show_help():

    print(Fore.GREEN + """Available commands:
    - n / s / e / w : move in a direction
    - map : show a map of the labyrinth
    - look : look around and describe you environment
    - use / equip <item> : use an item from your inventory
    - unequip <item> : stop using an item from your inventory
    - fight : attack a foe
    - examine <object> : examine an object more closely
    - get <item> : pick up an item
    - drop <item> : drop an item
    - r / rest : restore health by resting
    - inv / inventory : show current inventory
    - status : show current player status
    - q / quit : end the game""")


def draw_ui(current_game: Game):
    # print info across the entire window
    with current_game.term.location(0, 0):
        for i in range(current_game.term.width):
            print(current_game.term.on_green(' '), end="")

    # write health status on top of bar
    with current_game.term.location(5, 0):
        print(current_game.term.black_on_green(f"Health: {current_game.player.hp}/{cfg.PLAYER_HP}"))

    # monsters defeated
    with current_game.term.location(45, 0):
        print(current_game.term.black_on_green(f"Monsters defeated: "
                                               + f"{current_game.player.monsters_defeated}/"
                                               + f"{current_game.num_monsters}"))

    # write xp
    with current_game.term.location(90, 0):
        print(current_game.term.black_on_green(f"XP: {current_game.player.xp}"))
