from flask import Blueprint, render_template, request, redirect, jsonify, session
from services.chatgpt_service import send_to_api
from services.file_manager import read_prompt, append_to_prompt, read_terminal_output
from services.chatgpt_service import send_directory_to_api
import os
from services.directory_processor import get_directory_structure_and_content
from config import Config

PROMPT_FILE = Config.PROMPT_FILE

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET"])
def index():
    model = session.get('model', 'gpt-4o-mini')
    current_prompt = read_prompt()
    terminal_output = read_terminal_output()  # Read terminal output for display
    return render_template(
        "index.html",
        model=model,
        current_prompt=current_prompt,
        terminal_output=terminal_output,
    )

@app_routes.route("/add_and_send", methods=["POST"])
def add_and_send():
    new_text = request.form.get("new_text", "").strip()
    directory_path = request.form.get("directory_path", "").strip()
    model = request.form.get("model", "gpt-4o-mini")
    session['model'] = model  # Save model in session
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
    send_to_api(model)
    return redirect("/")

@app_routes.route("/debug_directory", methods=["POST"])
def debug_directory():
    directory_path = request.json.get("directory_path")
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return jsonify({"error": "Invalid directory path"}), 400

    try:
        response = send_directory_to_api(directory_path, model)  # Pass the model
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_routes.route("/clear_prompt", methods=["POST"])
def clear_prompt():
    with open(PROMPT_FILE, "w") as f:
        f.write('')
    return jsonify({"message": "Prompt cleared successfully."}), 200
