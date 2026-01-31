"""Petit script pour exécuter la génération depuis la ligne de commande.
Usage: python run_example.py "Paris" 5 art food
"""
import sys
from pipeline import generate_itinerary


def main(argv):
    if len(argv) < 4:
        print("Usage: python run_example.py <destination> <duration> <interest1> [interest2 ...]")
        return
    destination = argv[1]
    duration = int(argv[2])
    interests = argv[3:]
    print(generate_itinerary(destination, duration, interests))


if __name__ == "__main__":
    main(sys.argv)
