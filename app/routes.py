from flask import Blueprint, render_template, request, redirect, jsonify, session
from services.chatgpt_service import send_to_api
from services.file_manager import read_prompt, append_to_prompt, read_terminal_output
import os
from services.directory_processor import get_directory_structure_and_content
from config import Config, system_role_definitions

PROMPT_FILE = Config.PROMPT_FILE
app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET"])
def index():
    model = session.get('model', 'gpt-4o-mini')
    system_role = session.get("system_role", "Linux system administrator")
    current_prompt = read_prompt()
    refresh_interval = session.get("refresh_interval", "disabled")  # Set default to "disabled"
    terminal_output = read_terminal_output()  # Read terminal output for display
    return render_template(
        "index.html",
        model=model,
        system_role=system_role,
        current_prompt=current_prompt,
        terminal_output=terminal_output,
        refresh_interval=refresh_interval,
        role_definitions=system_role_definitions,

    )

@app_routes.route("/add_and_send", methods=["POST"])
def add_and_send():
    new_text = request.form.get("new_text", "").strip()
    directory_path = request.form.get("directory_path", "").strip()
    model = request.form.get("model", "gpt-4o-mini")
    session['model'] = model  # Save model in session
    system_role = request.form.get("system_role", "Linux system administrator")
    session['system_role'] = system_role  # Save role in session
    send_terminal_output = request.form.get("send_terminal_output") == "yes"  # Check if the checkbox is checked

    if new_text:
        append_to_prompt(f"User: {new_text}")
        if send_terminal_output:
            terminal_output = read_terminal_output()  # Get the terminal output
            append_to_prompt(f"Terminal Output: {terminal_output}")  # Append it to the prompt         
    else:
        if send_terminal_output:
            terminal_output = read_terminal_output()  # Get the terminal output
            append_to_prompt(f"Terminal Output: {terminal_output}")  # Append it to the prompt    

    if directory_path:
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            append_to_prompt(f"Error: Invalid directory path: {directory_path}")
        else:
            directory_info = get_directory_structure_and_content(directory_path)
            append_to_prompt("Directory Structure and Contents:")
            append_to_prompt(f"Structure: {directory_info['structure']}")
            append_to_prompt(f"Contents: {directory_info['files']}")

    # Send the prompt to the API with the selected model
    send_to_api(model, system_role)
    return redirect("/")

@app_routes.route("/clear_prompt", methods=["POST"])
def clear_prompt():
    with open(PROMPT_FILE, "w") as f:
        f.write('')
    return jsonify({"message": "Prompt cleared successfully."}), 200

@app_routes.route("/get_models", methods=["GET"])
def get_models():
    try:
        import openai
        # ensure API key is set from config/env
        if not openai.api_key:
            openai.api_key = Config.OPENAI_API_KEY

        models_response = openai.Model.list()
        models = [m["id"] for m in models_response.get("data", [])]
        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

