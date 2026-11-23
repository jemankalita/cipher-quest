"""
Cipher Quest
A console code-breaking adventure for Code in Place.

You are a new recruit at the Secret Message Society. Each level hands you
an intercepted message scrambled with a classic cipher. Crack it to earn
points. Stuck? Buy a hint -- but hints cost points!

There is also a Cipher Workshop where you can encode your own secret
messages and even brute-force crack a Caesar cipher.
"""

import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
LEVEL_POINTS = 100
WRONG_GUESS_COST = 10
HINT_COST = 25
MIN_POINTS = 10

# Short proverbs and sayings used as secret messages.
MESSAGES = [
    "practice makes progress",
    "every expert was once a beginner",
    "small steps every day",
    "code is poetry for computers",
    "the best way to learn is to teach",
    "bugs are just puzzles in disguise",
    "keep calm and debug on",
    "curiosity is the engine of learning",
    "a journey of a thousand miles begins with one step",
    "knowledge grows when it is shared",
    "mistakes are proof that you are trying",
    "dream big and start small",
]


# ---------------------------------------------------------------- ciphers

def reverse_text(text):
    """Reverse the whole message: 'hello' -> 'olleh'."""
    return text[::-1]


def caesar_shift(text, shift):
    """Shift every letter forward by `shift` places, wrapping z -> a."""
    result = ""
    for ch in text:
        if ch in ALPHABET:
            new_index = (ALPHABET.index(ch) + shift) % 26
            result += ALPHABET[new_index]
        else:
            result += ch
    return result


def atbash(text):
    """Mirror the alphabet: a <-> z, b <-> y, c <-> x ..."""
    result = ""
    for ch in text:
        if ch in ALPHABET:
            result += ALPHABET[25 - ALPHABET.index(ch)]
        else:
            result += ch
    return result


def reverse_each_word(text):
    """Reverse each word but keep the word order: 'hi there' -> 'ih ereht'."""
    words = text.split(" ")
    return " ".join(word[::-1] for word in words)


# ---------------------------------------------------------------- levels

def build_levels():
    """Create the five levels, each with a fresh random message."""
    messages = random.sample(MESSAGES, 5)
    small_shift = random.randint(1, 3)
    big_shift = random.randint(4, 25)
    combo_shift = random.randint(1, 25)

    return [
        {
            "name": "Mirror Writing",
            "secret": messages[0],
            "coded": reverse_text(messages[0]),
            "hints": [
                "Try reading it from right to left.",
                "The first word is: " + messages[0].split()[0],
            ],
        },
        {
            "name": "Caesar's Little Step",
            "secret": messages[1],
            "coded": caesar_shift(messages[1], small_shift),
            "hints": [
                "Each letter moved forward a small number of places.",
                "The shift is " + str(small_shift) + ". Move each letter back.",
            ],
        },
        {
            "name": "Looking-Glass Alphabet",
            "secret": messages[2],
            "coded": atbash(messages[2]),
            "hints": [
                "The alphabet is flipped: a becomes z, b becomes y ...",
                "The first word is: " + messages[2].split()[0],
            ],
        },
        {
            "name": "Caesar's Giant Leap",
            "secret": messages[3],
            "coded": caesar_shift(messages[3], big_shift),
            "hints": [
                "It's a Caesar shift. Try the Workshop's brute-force cracker!",
                "The shift is " + str(big_shift) + ".",
            ],
        },
        {
            "name": "The Double Lock",
            "secret": messages[4],
            "coded": reverse_each_word(caesar_shift(messages[4], combo_shift)),
            "hints": [
                "Two tricks: every word is backwards AND letters are shifted.",
                "The shift is " + str(combo_shift) + ".",
            ],
        },
    ]


# ---------------------------------------------------------------- helpers

def clean(text):
    """Lowercase and keep only letters and single spaces, for fair comparison."""
    kept = ""
    for ch in text.lower():
        if ch in ALPHABET or ch == " ":
            kept += ch
    return " ".join(kept.split())


def ask_choice(prompt, valid_choices):
    """Keep asking until the user types one of the valid choices."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid_choices:
            return answer
        print("Please type one of: " + ", ".join(valid_choices))


def ask_int(prompt, low, high):
    """Ask for a whole number between low and high (inclusive)."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        print("Please enter a number from " + str(low) + " to " + str(high) + ".")


def print_banner():
    print()
    print("+-------------------------------------------+")
    print("|          C I P H E R   Q U E S T          |")
    print("|  a code-breaking adventure in the console |")
    print("+-------------------------------------------+")


# ---------------------------------------------------------------- campaign

def play_level(number, level):
    """Play one level. Returns the points earned (0 if the player gives up)."""
    points = LEVEL_POINTS
    hints_used = 0
    print()
    print("=== Level " + str(number) + ": " + level["name"] + " ===")
    print("Intercepted message:")
    print("    " + level["coded"].upper())
    print("Type your guess, or 'hint' (-" + str(HINT_COST)
          + " pts) or 'skip' to give up.")

    while True:
        guess = input("Your decoded message: ")
        command = guess.strip().lower()
        if command == "hint":
            if hints_used < len(level["hints"]):
                print("HINT: " + level["hints"][hints_used])
                hints_used += 1
                points = max(MIN_POINTS, points - HINT_COST)
            else:
                print("No hints left -- you've got this!")
        elif command == "skip":
            print("The message was: " + level["secret"])
            return 0
        elif clean(guess) == clean(level["secret"]):
            print("CRACKED! +" + str(points) + " points.")
            return points
        else:
            points = max(MIN_POINTS, points - WRONG_GUESS_COST)
            print("Not quite. Level worth is now " + str(points) + " points.")


def rank_for(score):
    """Turn a final score into a fun title."""
    if score >= 450:
        return "Grandmaster Codebreaker"
    if score >= 350:
        return "Senior Cryptanalyst"
    if score >= 200:
        return "Field Agent"
    if score > 0:
        return "Apprentice Decoder"
    return "Recruit (try again!)"


def play_campaign():
    levels = build_levels()
    total = 0
    for i in range(len(levels)):
        total += play_level(i + 1, levels[i])
        print("Total score: " + str(total))
    max_score = LEVEL_POINTS * len(levels)
    print()
    print("*** Mission complete! ***")
    print("Final score: " + str(total) + " / " + str(max_score))
    print("Your rank:   " + rank_for(total))


# ---------------------------------------------------------------- workshop

def crack_caesar(coded):
    """Show the message under all 25 possible shifts."""
    print("Trying every possible shift:")
    for shift in range(1, 26):
        attempt = caesar_shift(coded, -shift)
        print("  shift " + str(shift).rjust(2) + ": " + attempt)
    print("Look for the line that reads like real words!")


def workshop():
    print()
    print("=== Cipher Workshop ===")
    while True:
        print()
        print("1) Caesar encode   2) Caesar decode   3) Atbash")
        print("4) Reverse         5) Crack a Caesar  6) Back to menu")
        choice = ask_choice("Pick a tool: ", ["1", "2", "3", "4", "5", "6"])
        if choice == "6":
            return
        text = input("Enter your message: ").lower()
        if choice == "1":
            shift = ask_int("Shift (1-25): ", 1, 25)
            print("Encoded: " + caesar_shift(text, shift))
        elif choice == "2":
            shift = ask_int("Shift (1-25): ", 1, 25)
            print("Decoded: " + caesar_shift(text, -shift))
        elif choice == "3":
            print("Result: " + atbash(text))
        elif choice == "4":
            print("Result: " + reverse_text(text))
        else:
            crack_caesar(text)


# ---------------------------------------------------------------- menu

def show_rules():
    print()
    print("HOW TO PLAY")
    print("- There are 5 levels. Each scrambled message is worth up to "
          + str(LEVEL_POINTS) + " points.")
    print("- A wrong guess costs " + str(WRONG_GUESS_COST)
          + " points; a hint costs " + str(HINT_COST) + ".")
    print("- A cracked level is always worth at least " + str(MIN_POINTS)
          + " points.")
    print("- Capitals and punctuation don't matter in your guess.")
    print("- The Workshop has tools to help -- including a Caesar cracker!")


def main():
    print_banner()
    print("Welcome, recruit. The Secret Message Society needs your brain.")
    while True:
        print()
        print("1) Start mission   2) Cipher Workshop   3) How to play   4) Quit")
        choice = ask_choice("> ", ["1", "2", "3", "4"])
        if choice == "1":
            play_campaign()
        elif choice == "2":
            workshop()
        elif choice == "3":
            show_rules()
        else:
            print("Goodbye, agent. Keep your secrets safe!")
            return


if __name__ == "__main__":
    main()
