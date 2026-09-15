import os

#constants
BASE_DB_PATH = "botc.db"
BASE_IMAGE_DIR = "base_images"
BASE_SVG_DIR = "base_svgs"
TOKEN_SIZE = 2.0  # inches -- matches the circle's diameter
TOKEN_BUFFER = TOKEN_SIZE + .1

#input helpers
def yes_no():
    yes_options = ["y", "yes"]
    no_options = ["n", "no"]

    reply = input("Yes or No? ").lower().strip()
    if reply in yes_options:
        return True
    elif reply in no_options:
        return False
    else:
        print("Invalid input. Try again. \n")
        return yes_no()

def ask_filepath():
    reply = input("File path: ").strip()
    correct = os.path.isfile(reply)
    if correct:
        return reply
    else:
        print("Invalid input or file does not exist. Try again. \n")
        return ask_filepath()

def ask_number():
    reply = input("Number: ").strip()
    try:
        return float(reply.replace(" ", "").replace(",", ""))
    except ValueError:
        print("Invalid input, not a number. Try again. \n")
    return ask_number

def ask_text(question):
    return input(f"{question} : ").strip()

#other helpers
def ensure_dir(filepath):
    d = os.path.dirname(filepath)
    if d:
        os.makedirs(d, exist_ok=True)
