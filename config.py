import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key")
    PROMPT_FILE = "../prompt.txt"
    TERMINAL_OUTPUT_FILE = "../terminal_output.txt"