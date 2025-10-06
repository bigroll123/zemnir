import openai
from config import Config, system_role_definitions
from services.file_manager import read_prompt, append_to_prompt, write_terminal_output, truncate_prompt_file
from services.terminal_runner import extract_and_run_terminal_commands

# Ensure OpenAI key is set from config/env
if not getattr(openai, "api_key", None):
    openai.api_key = Config.OPENAI_API_KEY

def send_to_api(model, system_role, max_lines=3000):
    print(f"Using model: {model} and role: {system_role}")
    truncate_prompt_file(max_lines)

    prompt = read_prompt()
    prompt = "\n".join(" ".join(line.replace("\t", " ").split()) for line in prompt.splitlines() if line.strip())

    long_system_role = system_role_definitions.get(system_role, "")

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": long_system_role},
                {"role": "user", "content": prompt},
            ],
            request_timeout=30,
        )
        assistant_msg = response.choices[0].message.content
    except Exception as e:
        err = f"Error contacting OpenAI API: {e}"
        print(err)
        append_to_prompt(f"Assistant: {err}")
        write_terminal_output(err)
        return

    append_to_prompt(f"Assistant: {assistant_msg}")
    terminal_output = extract_and_run_terminal_commands(assistant_msg)
    write_terminal_output(terminal_output)

