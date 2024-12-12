import sys
sys.pycache_prefix = "/tmp/zemnir_pycache"
import requests
import time
import argparse
from config import Config


CERT_FILE = Config.CERT_FILE
KEY_FILE = Config.KEY_FILE

API_URL = "https://localhost:8443/add_and_send"
CLEAR_PROMPT_URL = "https://localhost:8443/clear_prompt"

# Helper functions
def send_request(model, text=None, directory_path=None, send_terminal_output=True):
    payload = {
        "new_text": text or "",  # Default to empty string if not provided
        "directory_path": directory_path or "",  # Default to empty string if not provided
        "model": model,
        "send_terminal_output": "yes" if send_terminal_output else "no"
    }
    response = requests.post(API_URL, data=payload, verify=False)  # Set verify=False for testing
    return response.status_code, response.text

def clear_prompt():
    response = requests.post(CLEAR_PROMPT_URL, verify=False)  # Set verify=False for testing
    return response.status_code, response.text

def print_file_contents(file_path):
    try:
        with open(file_path, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Example function for headless operation
def run_headless(model, text=None, directory_path=None, send_terminal_output=True):
    status_code, response = send_request(model, text, directory_path, send_terminal_output)
    if status_code == 200:
        print("Request sent successfully.")
    else:
        print(f"Failed to send request: {response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the app in headless mode.")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--text", type=str, help="Text to add to the prompt")
    parser.add_argument("--directory", type=str, help="Directory path for debugging")
    parser.add_argument("--interval", type=int, help="Auto-refresh interval in seconds")
    parser.add_argument("--send-terminal-output", action="store_true", help="Send terminal output flag")
    
    args = parser.parse_args()
    if args.interval is None:
        # Run once if no interval is specified
        run_headless(args.model, args.text, args.directory)
        print_file_contents("../prompt.txt")
        print_file_contents("../terminal_output.txt")
    else:
        try:
            while True:
                run_headless(args.model, args.text, args.directory)
                print_file_contents("../prompt.txt")
                print_file_contents("../terminal_output.txt")
                print("Sleeping for next interval...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Stopping headless operation.")
            clear_prompt()

