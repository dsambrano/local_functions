import enum
import itertools
import random
import time
import subprocess
import sys
import select
from gtts import gTTS

# import pyttsx

WAIT_TIME = 2


class CardSuits(enum.Enum):
    SPADE = "S"  # "♠"
    HEART = "H"  # "♥"
    DIAMOND = "D"  # "♦"
    CLOVER = "C"  # "♣"

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
    TEN = 0
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


def suits_color(suit: CardSuits):
    return "BLACK" if suit in (CardSuits.SPADE, CardSuits.CLOVER) else "RED"


def input_timeout(time: int):
    i, o, e = select.select([sys.stdin], [], [], time)
    input_text = sys.stdin.readline().strip()
    print("You said: ", input_text)


def play_mp3(file: str):
    subprocess.run(
        ["mpg321", file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def create_speech(string: str, filename: str = "pokeno.mp3"):
    language = "en"
    myobj = gTTS(text=string, lang=language, slow=False)
    myobj.save(filename)


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
            string = f"The {color} {card[0]} of {card[1]}."
            print(string)
            string = string * 2
        else:
            string = "Deck is empty"

        create_speech(string)
        play_mp3("pokeno.mp3")
        # subprocess.run(["say", string])

        ##  https://pythonprogramminglanguage.com/text-to-speech/
        # engine = pyttsx.init()
        # engine.say(string)
        # engine.runAndWait()


def main():
    deck = Deck()
    deck.shuffle()
    while deck.full_deck:
        deck.read_card()
        time.sleep(WAIT_TIME)
    print("All Cards are gone, you should start a new game")


if __name__ == "__main__":
    main()