import os
from config import Config
PROMPT_FILE = Config.PROMPT_FILE
TERMINAL_OUTPUT_FILE = Config.TERMINAL_OUTPUT_FILE

def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def append_to_prompt(text):
    with open(PROMPT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{text}\n")

def read_terminal_output():
    if os.path.exists(TERMINAL_OUTPUT_FILE):
        with open(TERMINAL_OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return "No terminal output yet."

def write_terminal_output(output):
    with open(TERMINAL_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)
