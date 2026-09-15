from api_calls import main as api_fill_db
from backside_decorations import main as create_engraved_back
from shared import ask_filepath, ask_number, ask_text, yes_no
from spreadsheet_reader import main as read_spreadsheet
from svgmaker import main as create_token_board


def classic_path(**kwargs):
    api_fill_db()
    create_token_board(kwargs)

def custom_path(**kwargs):
    script_name = ask_text("What is the script's name?")
    print("Enter the path to the .xlsx or .csv file with the token information.\n")
    file = ask_filepath()
    xlsx = yes_no("Is the file a .xlsx file? (If not, should be .csv) Yes/No")
    print("If you get a permissions error soon, ensure you do not have the file open that it is trying to read from.\n")
    read_spreadsheet(file, script_name, xlsx)
    create_token_board(True, script_name=script_name, width=kwargs.get("width"), height=kwargs.get("height"), new_only=kwargs.get("new_only"))

def decorate_path(**kwargs):
    print("Note that the file you use for decoration here should probably be a square.\n")
    print("Ensure its lines will engrave and not cut.\n")
    path = ask_filepath()
    name = ask_text("What name should the resulting svg be saved under?")
    create_engraved_back(path=path, name=name, width=kwargs.get("width"), height=kwargs.get("height"))

def print_welcome():
    pass

def mode_select(**kwargs):
    print("Type 'classic' to gather and print all tokens from the base game and carousel\n")
    print("Type 'custom' to gather and print all tokens from your uploaded .xlsx or .csv file\n")
    print("Type 'decorate' to use your uploaded image file to make an svg to engrave on back of tokens\n")
    set_to_print = ask_text("Option").lower()

    if set_to_print == "classic":
        classic_path(kwargs)
    elif set_to_print == "custom":
        custom_path(kwargs)
    elif set_to_print == "decorate":
        decorate_path(kwargs)
    else:
        print("Invalid input, retry.\n\n")
        mode_select(kwargs)

def main():
    print_welcome()

    width:float = ask_number("What board width do you want in inches?")
    height:float = ask_number("What board height do you want in inches?")
    print("Do you want to only print new ones (ones that have not been made into svg before)\n")
    new_only:bool = yes_no("Yes/No")

    mode_select(width=width, height=height, new_only=new_only)    
    
if __name__ == "__main__":
    main()
