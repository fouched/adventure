import game

from blessed import Terminal


def main():
    # clear terminal
    term = Terminal()
    print(term.clear())

    # play game until game over or player quits
    game.play_game()

if __name__ == "__main__":
    main()
