import sys
import games


def main():
    if sys.argv[1].__eq__("--displayAllActions"):
        if len(sys.argv) > 2:
            games.display_all_actins((int)(sys.argv[2]))
        else: games.display_all_actins()

    if sys.argv[1].__eq__("--methodical"):
        if len(sys.argv) > 2:
            games.methodical((int)(sys.argv[2]))
        else: games.methodical()

    if sys.argv[1].__eq__("H") and len(sys.argv) == 2:
        games.H(1)

    if sys.argv[1].__eq__("H") and len(sys.argv) > 2 and sys.argv[2].__eq__("--ahead"):
        games.H((int(sys.argv[3])))

if __name__ == "__main__":
    main()
