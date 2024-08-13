def welcome():
    print("                                                  DUNGEON")
    print("""
    The village of Honeywood has been terrorized by strange, deadly creatures for months now. Unable to endure any 
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with a longsword and a bundle of torches, you descend into the labyrinth, 
    ready to do battle....
        
    """)


def play_game():
    welcome()
    # get player input
    input("Press enter to begin...")
    explore_labyrinth()


def explore_labyrinth():
    while True:
        player_input = input("-> ")

        # process input
        if player_input == "help":
            print("Show help")

        elif player_input == "quit":
            print("Overcome with terror, you flee the dungeon.")
            # TODO: print out final score
            play_again()

        else:
            print("I'm not sure what you mean... type help for help.")


def play_again():
    yn = input("Play again? (yes/no) -> ")
    if yn == "yes":
        play_game()
    else:
        print("Until next time, adventurer.")
        exit(0)