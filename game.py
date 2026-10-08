import utils
from datetime import datetime, timedelta
import sys

def show_help():
    print("\033[33m=\033[0m"*50+'\n'+'\033[32mDD/MM/YYYY\033[0m : returns the clue of the day DD/MM/YYYY\n'
          '\033[32mtoday\033[0m : play the clue of the day\n'
          '\033[32mnext\033[0m : play the next unsolved clue\n'
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
        user_input = input(utils.rainbow_rgb('Welcome to Minute Cryptic CLI (type "help" for commands): '))

        match user_input.strip().lower().split():
            case ["quit"] | ["exit"]:
                break
            case ["help"]:
                show_help()
            case ["today"]:
                today = datetime.now().strftime("%d/%m/%Y")
                game_handler(today)
            case ["next"]:
                date = utils.get_last_unsolved_clue()
                game_handler(date)
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
                print("\033[33m=\033[0m"*50+'\n'+str(utils.get_hint(date, "keys"))+'\n' + "\033[33m=\033[0m"*50)
            case ["hint", num]:
                num_int = None
                try:
                    num_int = int(num)
                except:
                    print("<num> must be an integer !\n" +"\033[33m=\033[0m"*50)
                if num_int != None:
                    hints_count = len(utils.get_hint(date, "keys"))
                    if num_int > hints_count or num_int <= 0:
                        print("\033[33m=\033[0m"*50+'\n'+f"Choose the right bounds for <num>, here [1, {hints_count}]\n" +"\033[33m=\033[0m"*50)
                    else:
                        print("\033[33m=\033[0m"*50+ "\n" +utils.get_hint(date, "values", num_int) + "\n"+"\033[33m=\033[0m"*50)
            case ["help"]:
                show_in_game_help()
            case ["quit"] | ["exit"]:
                sys.exit()
            case [*words] if words:
                proposed_answer = " ".join(words)
                result = utils.check_answer(date, proposed_answer)
                if not result:
                     print("\033[33m=\033[0m"*50+'\n'+"\033[31mWrong answer, try again !\033[0m\n" + "\033[33m=\033[0m"*50)
                else:
                    print("\033[33m=\033[0m"*50+'\n'+utils.rainbow_rgb("Well done ! It's the right answer !")+"\n" + "\033[33m=\033[0m"*50)
                    
                    utils.set_solved_clue(date)
                    
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

    clue = utils.get_clue(date)

    if clue == None:
        print("\033[33m=\033[0m"*50+'\n'+"Try again !\n" + "\033[33m=\033[0m"*50)
    else:
        print("\033[33m=\033[0m"*50+'\n'+f"The clue of {date} is :\n\033[35m{clue}\033[0m\n" +"\033[33m=\033[0m"*50)
        clue_handler(clue, date)

        
                

if __name__ == "__main__":
    start_game_handler()
