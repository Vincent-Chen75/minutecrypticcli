from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime
import re
import base64

URL = "https://www.minutecryptic.com/"
JSON_FILE = "minutecryptic.json"

def save_puzzle_to_json(
    clue: str, hints_dict: dict, answer: str, file_path: str = JSON_FILE
):
    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    if any(item.get("clue") == clue for item in data):
        print(f"Clue already in JSON : '{clue}'")
        return

    data.append(
        {
            "clue": clue,
            "date": datetime.now().strftime("%d/%m/%Y"),
            "hints": hints_dict,
            "answer":answer,
            "solved":False,
        }
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Added to JSON : '{clue}'")

def answer_size(string: str):
    match = re.search(r"\(([\d,]+)\)\s*$", string)

    if not match:
        return None
    numbers = [int(n) for n in match.group(1).split(",")]

    return numbers[0] if len(numbers) == 1 else numbers

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    page.get_by_text("not now", exact=True).click()
    
    clue_locator = page.locator("p.leading-8").first
    clue_locator.wait_for(state="visible")
    clue = clue_locator.inner_text().strip()

    size = answer_size(clue)

    page.get_by_text("play", exact=True).click()
    page.get_by_text("hints", exact=True).click(force=True)

    modal_selector = 'div[role="dialog"], [data-sentry-component="Modal"]'
    page.wait_for_selector(modal_selector, state="visible", timeout=5000)
    page.wait_for_timeout(300)
    
    raw_extracted_hints = {}

    page.wait_for_timeout(300)
    buttons_locator = page.locator('div[role="dialog"] button:has(p)')
    button_count = buttons_locator.count()

    for i in range(button_count-1):
        btn = buttons_locator.nth(i)
        btn_label = btn.inner_text().strip()

        btn.click(force=True)
        page.wait_for_timeout(400)

        hint_paragraph = page.locator(
            'div[role="dialog"] p, [data-sentry-component="Modal"] p'
        ).last
        if hint_paragraph.is_visible(timeout=1500):
            hint_text = hint_paragraph.inner_text().strip()
        else:
            hint_text = ""

        raw_extracted_hints[btn_label.lower()] = base64.b64encode(hint_text.encode("utf-8")).decode("utf-8")

        page.keyboard.press("Escape")
        page.get_by_text("hints", exact=True).click(force=True)

        page.wait_for_timeout(300)

    if type(size) == int:
        count = size
    elif type(size) == list:
        count = sum(size)

    for _ in range(count):
        page.get_by_text("show letter", exact=True).click(force=True)

    spans = page.locator('span.-translate-y-1.px-2')

    answer = ""
    if spans.count() == count:
        for i in range(count):
            span = spans.nth(i)
            letter = span.inner_text().strip()
            answer += letter

    if (len(answer) != count):
        raise ValueError(f"Mismatch between answer length ({len(answer)}) and clue count ({count})")
    
    answer_encoded = base64.b64encode(answer.encode("utf-8")).decode("utf-8")
    
    browser.close()
    save_puzzle_to_json(clue, raw_extracted_hints, answer_encoded)