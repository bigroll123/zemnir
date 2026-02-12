import google.generativeai as genai
from config import Config, system_role_definitions
from services.file_manager import read_prompt, append_to_prompt, write_terminal_output, truncate_prompt_file
from services.terminal_runner import extract_and_run_terminal_commands

# Ensure Gemini API key is set
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)

def send_to_api(model_name, system_role, max_lines=3000):
    print(f"Using model: {model_name} and role: {system_role}")
    truncate_prompt_file(max_lines)

    prompt = read_prompt()
    # Clean up prompt whitespace and filter empty lines
    prompt = "\n".join(" ".join(line.replace("\t", " ").split()) for line in prompt.splitlines() if line.strip())

    if not prompt:
        print("Prompt is empty. Skipping API call.")
        return

    long_system_role = system_role_definitions.get(system_role, "")

    try:
        # Build arguments dynamically to avoid passing empty system_instruction
        model_kwargs = {"model_name": model_name}
        if long_system_role:
            model_kwargs["system_instruction"] = long_system_role

        model = genai.GenerativeModel(**model_kwargs)
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Check if the response contains text (handles safety blocks gracefully)
        if response.parts:
            assistant_msg = response.text
        else:
            assistant_msg = "Error: No response generated. The prompt may have triggered safety filters."

    except Exception as e:
        err = f"Error contacting Gemini API: {e}"
        print(err)
        append_to_prompt(f"Assistant: {err}")
        write_terminal_output(err)
        return

    append_to_prompt(f"Assistant: {assistant_msg}")
    terminal_output = extract_and_run_terminal_commands(assistant_msg)
    write_terminal_output(terminal_output)