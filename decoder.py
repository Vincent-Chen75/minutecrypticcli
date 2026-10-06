import base64
import json
import os

JSON_FILE = "minutecryptic.json"

def hint_decoder(string):
    return base64.b64decode(string.encode("utf-8")).decode("utf-8")

def get_clue(date_string:str, file_path:str = JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        if date_string.strip().lower() in entry.get("date").lower():
            clue = entry.get("clue")
            return clue
    
    print(f"No clue found for {date_string}")
    return None
    

def get_answer(clue:str, file_path:str = JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        if clue.strip().lower() in entry.get("clue", "").lower():
            answer = entry.get("answer")
            return answer

    print("No clue found in database")
    return None

def check_answer(clue:str, proposed_answer):
    real_answer = hint_decoder(get_answer(clue))
    return real_answer.strip().lower() == proposed_answer.strip().lower()

def get_hint(clue:str, type:str, file_path:str = JSON_FILE, *args):
    if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas !")
            return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        if clue.strip().lower() in entry.get("clue", "").lower():
            hints = entry.get("hints")
            if type=="keys":
                return list(hints.keys())
            elif type=="values":
                return hint_decoder(list(hints.values())[int(args[0])-1])
            else:
                print("Type is wrong !")
                return None
    print("No clue found in database")
    return None