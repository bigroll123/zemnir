import openai
from services.file_manager import read_prompt, append_to_prompt, write_terminal_output
from services.terminal_runner import extract_and_run_terminal_commands
from services.directory_processor import get_directory_structure_and_content

# openai.api_key = "YOUR_API_KEY"  # Replace or use an environment variable


def send_to_api(model):
    print(f"Using model: {model}")  # Print the current model

    # Step 1: Read the current prompt

    prompt = read_prompt()

    # Step 2: Send the prompt to OpenAI's API

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Linux system administrator, DevOps engineer, and software developer, You are strict, responsible for monitoring, support, coding, and optimizing existing code. Whenever you are prompted for hardware/software questions first assume you need to provide Linux commands. All commands must be enclosed between START_TERMINAL99 and END_TERMINAL99 this is mandatory, with no additional formatting. Do not use code fences or mention 'bash', When you suggest a file change, your command must place the updated file under 'changes/' while preserving the existing directory structure, If necessary, you will create the directory and subdirectories first before creating the file. Do not write bash scripts unless you are prompted, provide just the commands"},
            {"role": "user", "content": prompt},
        ],
    )
    assistant_msg = response.choices[0].message.content

    # Step 3: Append the assistant's response to the prompt

    append_to_prompt(f"Assistant: {assistant_msg}")

    # Step 4: Extract and run terminal commands from the assistant's response

    terminal_output = extract_and_run_terminal_commands(assistant_msg)

    # Step 5: Write the terminal output to a file

    write_terminal_output(terminal_output)

def send_directory_to_api(directory_path, model):
    print(f"Using model for directory: {model}")  # Print the selected model

    # Get directory structure and file content

    directory_info = get_directory_structure_and_content(directory_path)

    # Format the data for sending

    formatted_message = (
        f"Directory Structure:\n{directory_info['structure']}\n\n"
        f"File Contents:\n{directory_info['files']}"
    )

    # Send to OpenAI API

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Linux system administrator, DevOps engineer, and software developer, You are strict, responsible for monitoring, support, coding, and optimizing existing code. Whenever you are prompted for hardware/software questions first assume you need to provide Linux commands. All commands must be enclosed between START_TERMINAL99 and END_TERMINAL99 this is mandatory, with no additional formatting. Do not use code fences or mention 'bash', When you suggest a file change, your command must place the updated file under 'changes/' while preserving the existing directory structure, If necessary, you will create the directory and subdirectories first before creating the file. Do not write bash scripts unless you are prompted, provide just the commands"},
            {"role": "user", "content": formatted_message},
        ],
    )
    return response.choices[0].message.content
