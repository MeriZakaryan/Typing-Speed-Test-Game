import json
import time
import datetime
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
                "easy": [
                    "Be yourself; everyone else is already taken.",
                    "A room without books is like a body without a soul.",
                ],
                "medium": [
                    "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
                    "Be who you are and say what you feel, because those who mind don't matter, and those who matter don't mind."
                ],
                "hard": [
                    "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do. So throw off the bowlines. Sail away from the safe harbor. Catch the trade winds in your sails. Explore. Dream. Discover.",
                    "The TV business is uglier than most things. It is normally perceived as some kind of cruel and shallow money trench through the heart of the journalism industry, a long plastic hallway where thieves and pimps run free and good men die like dogs, for no good reason.",
                ]
            }
        }


def get_history():
    try:
        with open(HISTORY_JSON, "r") as history_file:
            content = history_file.read()
            if not content.strip():
                return []  # File is empty
            return json.loads(content)
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


def start_game(data, history):
    print("\n Choose level difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("Enter your choice [1-3]: ")
    if choice == "1":
        level = "easy"
    elif choice == "2":
        level = "medium"
    elif choice == "3":
        level = "hard"
    else:
        print("Invalid choice. Try again.")
        return

    text = random.choice(data["sample_texts"][level])
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
    print("-"*100)
    print(f"WPM(Word per minute): {wpm:.2f}")
    print(f"Word Accuracy: {word_accuracy:.2f}%")
    print(f"Character Accuracy: {char_accuracy:.2f}%")

    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history.append({
        "difficulty": level,
        "wpm": round(wpm, 2),
        "word_accuracy": round(word_accuracy, 2),
        "char_accuracy": round(char_accuracy, 2),
        "date": current_date
    }) 

    if len(history) > data["history_limit"]:
        history.pop(0)

    save_history(history)
    print("Test data saved to history.\n")


def view_history(history):
    print("\nGame History")
    print("-"*100)

    if not history:
        print("No history available.")
        return
    
    for entry in history:
        print(f"Difficulty Level: {entry['difficulty']}")
        print(f"WPM: {entry['wpm']}")
        print(f"Word Accuracy: {entry['word_accuracy']}%")
        print(f"Character Accuracy: {entry['char_accuracy']}%")
        print(f"Date: {entry['date']}\n")


def change_limit(data):
    try:
        new_limit = int(input("Enter new limit (e.g. 3): "))
        if new_limit <= 0:
            print("History limit should be greater than 0.")
            return
        data["history_limit"] = new_limit
        save_data(data)
        print("History limit updated.\n")
    except ValueError:
        print("Invalid input. Enter a number.")


def main():
    data = get_data()
    history = get_history()     

    while(True):    
        print("\n====== Typing Speed Test Game ======")
        print("1. Take a Typing Test")
        print("2. View History")
        print("3. Change History Limit")
        print("4. Exit")
        
        choice = input("Enter your choice [1-4]: ")
        if choice == "1":
            start_game(data, history)
        elif choice == "2":
            view_history(history)
        elif choice == "3":
            change_limit(data)
        elif choice == "4":
            print("\nGoodbye!!!!")
            break
        else:
            print("Invalid option. Try again.")

main()