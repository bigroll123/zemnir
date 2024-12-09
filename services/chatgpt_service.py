import openai
from services.file_manager import read_prompt, append_to_prompt, write_terminal_output
from services.terminal_runner import extract_and_run_terminal_commands
from services.directory_processor import get_directory_structure_and_content

#openai.api_key = "YOUR_API_KEY"  # Replace or use an environment variable

def send_to_api():
    # Step 1: Read the current prompt
    prompt = read_prompt()

    # Step 2: Send the prompt to OpenAI's API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
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

def send_directory_to_api(directory_path):
    # Get directory structure and file content
    directory_info = get_directory_structure_and_content(directory_path)

    # Format the data for sending
    formatted_message = (
        f"Directory Structure:\n{directory_info['structure']}\n\n"
        f"File Contents:\n{directory_info['files']}"
    )

    # Send to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for debugging."},
            {"role": "user", "content": formatted_message},
        ],
    )
    return response.choices[0].message.content