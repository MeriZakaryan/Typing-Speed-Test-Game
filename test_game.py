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

def calculate_reults(start, end, text, typed_text):
    passed_time = end - start
    if passed_time > 0:
        minutes = passed_time / 60
    else:
        minutes = 1

    sample_words = text.strip().split()
    player_words =  typed_text.strip().split()
    word_count = len(player_words)   
    wpm = word_count / minutes

    corrects = 0
    for player_word, sample_word in zip(player_words, sample_words):
        if player_word == sample_word:
            corrects += 1
    
    word_accuracy = corrects / len(sample_words) * 100

    corrects = 0
    total_chars = len(text)
    for char in range(min(len(typed_text), total_chars)):
        if typed_text[char] == text[char]:
            corrects += 1
    
    char_accuracy = corrects / total_chars * 100

    return wpm, word_accuracy, char_accuracy


def startGame(data, history):
    print("\n Choose level difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    level = input("Enter your choice [1-3]: ")
    if level == "1":
        quote_type = "short"
    elif level == "2":
        quote_type = "medium"
    elif level == "3":
        quote_type = "long"
    else:
        print("Invalid choice. Returning to menu.")
        return

    text = random.choice(data["sample_texts"][quote_type])
    print("\nHere is your text. Type as fast as you can! Pay attention to accuracy :)")
    print("\n" + "-"*100)
    print(text)
    print("-"*100)

    input("\nPress ENTER to start")
    print("Type below:\n")
    start = time.time()
    typed_text = input()
    end = time.time()

    wpm, word_accuracy, char_accuracy = calculate_reults(start, end, text, typed_text)

    print("\nResults")
    print("" + "-"*100)
    print(f"WPM(Word per minute): {wpm:.2f}")
    print(f"Word Accuracy: {word_accuracy:.2f}%")
    print(f"Character Accuracy: {char_accuracy:.2f}%")





def main():
    data = get_data()
    history = get_history()         

    # print(data)
    # print(history)
    startGame(data, history)

main()