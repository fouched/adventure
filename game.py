from classes import Player, Room, Game

from colorama import Fore, init


def welcome():
    print(Fore.RED + "                                                  D U N G E O N")
    print(Fore.GREEN + """
    The village of Honeywood has been terrorized by strange, deadly creatures for months now. Unable to endure any 
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with a longsword and a bundle of torches, you descend into the labyrinth, 
    ready to do battle....
        
    """)


def play_game():
    # init makes sure that colorama works on various platforms
    init()

    adventurer = Player()

    current_game = Game(adventurer)

    room = Room()

    current_game.room = room


    welcome()
    # get player input
    input("Press enter to begin...")
    explore_labyrinth(current_game)


def explore_labyrinth(current_game: Game):
    while True:
        current_game.room.print_description()

        player_input = input(Fore.YELLOW + "-> ").lower().strip()

        # process input
        if player_input == "help":
            show_help()

        elif player_input == "quit":
            print("Overcome with terror, you flee the dungeon.")
            # TODO: print out final score
            play_again()

        else:
            print("I'm not sure what you mean... type help for available commands.")


def play_again():
    yn = get_yn(Fore.CYAN + "Play again")
    if yn == "yes":
        play_game()
    else:
        print("Until next time, adventurer.")
        exit(0)


def get_yn(question: str) -> str:
    while True:
        answer = input(question + " (yes/no) -> ").lower().strip()
        if answer not in ["yes", "no", "y", "n"]:
            print("Please enter yes or no.")
        else:
            if answer == "y":
                answer = "yes"
            elif answer == "n":
                answer = "no"

            return answer


def show_help():
    print(Fore.GREEN + """Available commands:
    - n/s/e/w : move in a direction
    - map : show a map of the labyrinth
    - look : look around and describe you environment
    - equip <item> : use an item from your inventory
    - unequip <item> : stop using an item from your inventory
    - fight : attack a foe
    - examine <object> : examine an object more closely
    - get <item> : pick up an item
    - drop <item> : drop an item
    - rest : restore health by resting
    - inventory : show current inventory
    - status : show current player status
    - quit : end the game""")