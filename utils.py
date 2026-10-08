import base64
import json
import os
import math

JSON_FILE = "minutecryptic.json"

def hint_decoder(string:str):
    return base64.b64decode(string.encode("utf-8")).decode("utf-8")

def get_clue(date_string:str, file_path:str = JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        if date_string.strip() == entry.get("date", "").strip():
            return entry.get("clue")
    
    print(f"No clue found for {date_string}")
    return None
    

def get_answer(date:str, file_path:str = JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        if date.strip() == entry.get("date", "").strip():
            answer = entry.get("answer")
            return answer

    print("No clue found in database")
    return None

def check_answer(date:str, proposed_answer):
    real_answer = hint_decoder(get_answer(date))
    return real_answer.strip().lower() == proposed_answer.strip().lower()

def get_hint(date:str, type:str, *args, file_path:str = JSON_FILE):
    if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas !")
            return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        if date.strip() == entry.get("date", "").strip():
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

def get_last_unsolved_clue(file_path=JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        if not entry.get("solved"):
            return entry.get("date")

    print("No unsolved clue !")
    return None


def set_solved_clue(date, file_path=JSON_FILE):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas !")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = False
    for entry in data:
        if entry.get("date", "").strip().lower() == date.strip().lower():
            entry["solved"] = True
            updated = True
            break

    if updated:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


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