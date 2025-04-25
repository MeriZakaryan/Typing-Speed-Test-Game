import json
import time
from datetime import datetime
import random

DATA_JSON = "data.json"
HISTORY_JSON = "history.json"

def get_data():
    try:
        with open(DATA_JSON, "r") as data:
            return json.load(data)
    except FileNotFoundError:
        print("Game can not load properly. You have limited version :(")
        return {
            "history_limit": 5,
            "sample_texts": {
                "short": [
                    "Be yourself; everyone else is already taken.",
                    "A room without books is like a body without a soul.",
                ],
                "medium": [
                    "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
                    "Be who you are and say what you feel, because those who mind don't matter, and those who matter don't mind."
                ],
                "long": [
                    "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do. So throw off the bowlines. Sail away from the safe harbor. Catch the trade winds in your sails. Explore. Dream. Discover.",
                    "The TV business is uglier than most things. It is normally perceived as some kind of cruel and shallow money trench through the heart of the journalism industry, a long plastic hallway where thieves and pimps run free and good men die like dogs, for no good reason.",
                ]
            }
        }

def get_history():
    try:
        with open(HISTORY_JSON, "r") as history:
            if not history.read():
                return []  # Empty file fallback
            return json.loads(history.read())
    except FileNotFoundError:
        return []
    
def save_data(data):
    with open(DATA_JSON, 'w') as info:
        json.dump(data, info, indent=4)

def save_history(history):
    with open(HISTORY_JSON, 'w') as info:
        json.dump(history, info, indent=4)


def main():
    data = get_data()
    history = get_history()         

    # print(data)
    # print(history)

main()