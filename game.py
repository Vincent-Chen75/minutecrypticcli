import decoder
from datetime import datetime, timedelta
import sys
import math

JSON_FILE = "minutecryptic.json"

def rainbow_rgb(string:str):
    result = []
    for i, char in enumerate(string):
        if char == " ":
            result.append(" ")
            continue
        
        frequency = 0.3
        r = int(math.sin(frequency * i + 0) * 127 + 128)
        g = int(math.sin(frequency * i + 2) * 127 + 128)
        b = int(math.sin(frequency * i + 4) * 127 + 128)
        
        result.append(f"\033[38;2;{r};{g};{b}m{char}")

    result.append("\033[0m")
    return "".join(result)

def show_help():
    print("\033[33m=\033[0m"*50+'\n'+'\033[32mDD/MM/YYYY\033[0m : returns the clue of the day DD/MM/YYYY\n'
          '\033[32mtoday\033[0m : play the clue of the day\n'
          '\033[32mquit\033[0m or \033[32mexit\033[0m will stop the program\n' + "\033[33m=\033[0m"*50)

def show_in_game_help():
    print("\033[33m=\033[0m"*50+'\n'+'type in your answer or use the following commands\n'
          '\033[32mclue\033[0m to reprint the clue\n'
          '\033[32mhints\033[0m to show the existing hints available but not revealing it\n'
          '\033[32mhint <num>\033[0m to reveal the hint no. num\n'
          '\033[32mback\033[0m will return to the main menu\n'
          '\033[32mquit\033[0m or \033[32mexit\033[0m will stop the program\n' + "\033[33m=\033[0m"*50)

def start_game_handler():
    while True: 
        user_input = input(rainbow_rgb('Welcome to Minute Cryptic CLI (type "help" for commands): '))

        match user_input.strip().lower().split():
            case ["quit"] | ["exit"]:
                break
            case ["help"]:
                show_help()
            case ["today"]:
                today = datetime.now().strftime("%d/%m/%Y")
                game_handler(today)
            case[date]:
                game_handler(date)
            case []:
                continue
            case _:
                print("\033[33m=\033[0m"*50+'\n'+"Unknown commands !\n" + "\033[33m=\033[0m"*50)

def clue_handler(clue, date):
    while True:
        game_input = input(f'Clue of {date} (type "help" for commands): ')
    
        match game_input.strip().lower().split():
            case ["back"]:
                break
            case ["clue"]:
                print("\033[33m=\033[0m"*50+'\n'+f"The clue is :\n{clue}\n" +"\033[33m=\033[0m"*50)
            case ["hints"]:
                print("\033[33m=\033[0m"*50+'\n'+str(decoder.get_hint(clue, "keys"))+'\n' + "\033[33m=\033[0m"*50)
            case ["hint", num]:
                num_int = None
                try:
                    num_int = int(num)
                except:
                    print("<num> must be an integer !\n" +"\033[33m=\033[0m"*50)
                if num_int != None:
                    hints_count = len(decoder.get_hint(clue, "keys"))
                    if num_int > hints_count or num_int <= 0:
                        print("\033[33m=\033[0m"*50+'\n'+f"Choose the right bounds for <num>, here [1, {hints_count}]\n" +"\033[33m=\033[0m"*50)
                    else:
                        print(decoder.get_hint(clue, "values", JSON_FILE, num_int) + "\n"+"\033[33m=\033[0m"*50)
            case ["help"]:
                show_in_game_help()
            case ["quit"] | ["exit"]:
                sys.exit()
            case [proposed_answer]:
                result = decoder.check_answer(clue, proposed_answer)
                if not result:
                     print("\033[33m=\033[0m"*50+'\n'+"\033[31mWrong answer, try again !\033[0m\n" + "\033[33m=\033[0m"*50)
                else:
                    print("\033[33m=\033[0m"*50+'\n'+rainbow_rgb("Well done ! It's the right answer !")+"\n" + "\033[33m=\033[0m"*50)
                    end_game_input = input('What next ? \n'
                    '\033[32mmain\033[0m to go to the main menu\n' \
                    '\033[32mnext\033[0m to go to the next clue (by date)\n' \
                    '\033[32mprevious\033[0m to go to the previous clue (by date)\n' \
                    '\033[32mquit\033[0m or \033[32mexit\033[0m to exit the game\n'+ "\033[33m=\033[0m"*50+'\n')

                    match end_game_input.strip().lower().split():
                        case ["main"]:
                            start_game_handler()
                        case ["next"]:
                            next_date = datetime.strftime(datetime.strptime(date, "%d/%m/%Y") + timedelta(days=1), "%d/%m/%Y")
                            game_handler(next_date)
                        case ["previous"]:
                            previous_date = datetime.strftime(datetime.strptime(date, "%d/%m/%Y") - timedelta(days=1), "%d/%m/%Y")
                            game_handler(previous_date)
                        case ["quit"] | ["exit"]:
                            sys.exit()
            

def game_handler(date:str):
    try:
        date_val = datetime.strptime(date, "%d/%m/%Y")
    except:
        print("\033[33m=\033[0m"*50+'\n'+"Date format incorrect, needs to be in DD/MM/YYYY format !\n" + "\033[33m=\033[0m"*50)
        return 

    if date_val < datetime(2026,10,2):
        print("\033[33m=\033[0m"*50+'\n'+"Please provide a date after 02/10/2026 !\n" + "\033[33m=\033[0m"*50)
        start_game_handler()

    clue = decoder.get_clue(date)

    if clue == None:
        print("\033[33m=\033[0m"*50+'\n'+"Try again !\n" + "\033[33m=\033[0m"*50)
    else:
        print("\033[33m=\033[0m"*50+'\n'+f"The clue of {date} is :\n\033[35m{clue}\033[0m\n" +"\033[33m=\033[0m"*50)
        clue_handler(clue, date)

        
                

if __name__ == "__main__":
    start_game_handler()
