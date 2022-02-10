
import json
import sys
import readchar
from colorama import Fore, Style
import random
import unidecode

lang = "pt_BR"

terms = []
with open("words/{0}/terms.json".format(lang)) as f:
    terms = json.load(f)
    f.close()

terms_normalized = []
for term in terms:
    terms_normalized += [unidecode.unidecode(term).upper()]

answers = []
with open("words/{0}/answers.json".format(lang)) as f:
    answers = json.load(f)
    f.close()

answer = random.choice(answers)
answer_normalized = unidecode.unidecode(answer).upper()

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def check(word):
    right = 0
    if "".join(word) not in terms_normalized:
        right = -1
    else:
        for i in range(5):
            if answer_normalized[i] == word[i]:
                color = Fore.GREEN
                right += 1
            elif word[i] in answer_normalized:
                color = Fore.YELLOW
            else:
                color = Fore.LIGHTBLACK_EX
            try:
                index = ord(word[i]) - 65
                alphabet[index] = color_char(color, chr(index + 65))
            except ValueError:
                pass
            word[i] = color_char(color, word[i])
    return right


def color_char(color, char):
    return color + char + Fore.RESET


def generate_line(tries, word, alert):
    jump = ""
    if alert == "!":
        alert = color_char(Fore.RED, alert)
    elif alert == "✓":
        alert = color_char(Fore.GREEN, alert)
        jump = "\n"
    elif alert == "✗":
        alert = color_char(Fore.RED, alert)
        jump = "\n"
    msg = "\r{0}{1} - {2}{3}{4} |  {5}  | {6}{7}".format(Style.BRIGHT, tries+1, " ".join(word), " " if len(
        word) > 0 and len(word) < 5 else "", " ".join(["_"] * (5 - len(word))), alert, " ".join(alphabet), jump)
    return msg


tries = 0
while tries < 6:
    pos = 0
    word = []
    right = 0
    alert = " "
    enter = False
    sys.stdout.flush()
    sys.stdout.write(generate_line(tries, word, alert))
    while not enter:
        ch = readchar.readkey().upper()
        # Ctrl + C
        if ch == '\x03':
            exit(-1)
        # Backspace
        elif ch == '\x7f':
            if pos > 0:
                word.pop()
                pos -= 1
        if pos < 5:
            # Only letters
            if ch >= '\x41' and ch <= '\x5a':
                word += [ch.upper()]
                pos += 1
        else:
            # Enter
            if ch == '\x0d':
                # Check word
                right = check(word)
                if right == -1:
                    word = []
                    pos = 0
                    alert = "!"
                elif right == 5:
                    alert = "✓"
                    enter = True
                else:
                    alert = "✗"
                    enter = True
        sys.stdout.flush()
        sys.stdout.write(generate_line(tries, word, alert))
        alert = " "
    if right == 5:
        break
    else:
        tries += 1
sys.stdout.flush()
sys.stdout.write("\nResposta correta: {0}\n".format(answer.upper()))
