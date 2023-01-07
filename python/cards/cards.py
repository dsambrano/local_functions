import enum
import itertools
import random
import time
import pyttsx

WAIT_TIME = 2


class CardSuits(enum.Enum):
    SPADE = "♠"
    HEART = "♥"
    DIAMOND = "♦"
    CLOVER = "♣"

    def get_color(self):
        pass


class CardRanks(enum.Enum):
    ACE = "A"
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


def suits_color(suit: CardSuits):
    return "BLACK" if suit in (CardSuits.SPADE, CardSuits.CLOVER) else "RED"


class Deck:
    suits = (suit.name for suit in CardSuits)
    ranks = (rank.name for rank in CardRanks)
    full_deck = [(r[0], r[1]) for r in itertools.product(ranks, suits)]

    def shuffle(self):
        random.shuffle(self.full_deck)

    def get_top_card(self):
        return self.full_deck.pop(0)

    def get_bottom_card(self):
        return self.full_deck.pop(0)

    def read_card(self):
        if self.full_deck:
            card = self.get_top_card()
            color = suits_color(CardSuits[card[1]])
            string = f"{color} {card[0]} of {card[1]}"
        else:
            string = "Deck is empty"

        engine = pyttsx.init()
        engine.say(string)
        engine.runAndWait()


def main():
    deck = Deck()
    deck.shuffle()
    while deck.full_deck:
        deck.read_card()
        time.sleep(WAIT_TIME)
    print("All Cards are gone, you should start a new game")


if __name__ == "__main__":
    main()
