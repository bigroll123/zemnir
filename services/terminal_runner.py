import subprocess
import re

def extract_and_run_terminal_commands(text):
    """
    Extract commands between START_TERMINAL99 and END_TERMINAL99 tags and execute them.
    """
    # Regex pattern to extract the commands
    pattern = r"START_TERMINAL99(.*?)END_TERMINAL99"
    matches = re.findall(pattern, text, flags=re.DOTALL)  # Extract all matching command blocks

    terminal_output = ""  # To store the terminal output from all command blocks

    # Iterate through each command block
    for cmd_block in matches:
        cmd_block = cmd_block.strip()  # Clean up whitespace
        print(f"Executing Command Block: {cmd_block}")  # Debugging: Show extracted command
        try:
            # Execute the command using subprocess
            output = subprocess.check_output(cmd_block, shell=True, stderr=subprocess.STDOUT)
            terminal_output += output.decode('utf-8') + "\n"
        except subprocess.CalledProcessError as e:
            # Append error output to the terminal output
            terminal_output += f"Error executing command: {e.output.decode('utf-8')}\n"

    return terminal_output
