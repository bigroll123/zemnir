from flask import Blueprint, render_template, request, redirect, jsonify, session
from services.gemini_service import send_to_api
from services.file_manager import read_prompt, append_to_prompt, read_terminal_output
import os
from services.directory_processor import get_directory_structure_and_content
from config import Config, system_role_definitions

PROMPT_FILE = Config.PROMPT_FILE
app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET"])
def index():
    model = session.get('model', 'gemini-1.5-flash')
    # FIX: "System Administrator" matches the key in config.py
    system_role = session.get("system_role", "System Administrator")
    current_prompt = read_prompt()
    refresh_interval = session.get("refresh_interval", "disabled")
    terminal_output = read_terminal_output()
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
    model = request.form.get("model", "gemini-1.5-flash")
    session['model'] = model
    # FIX: "System Administrator" matches the key in config.py
    system_role = request.form.get("system_role", "System Administrator")
    session['system_role'] = system_role
    send_terminal_output = request.form.get("send_terminal_output") == "yes"

    if new_text:
        append_to_prompt(f"User: {new_text}")
        if send_terminal_output:
            terminal_output = read_terminal_output()
            append_to_prompt(f"Terminal Output: {terminal_output}")         
    else:
        if send_terminal_output:
            terminal_output = read_terminal_output()
            append_to_prompt(f"Terminal Output: {terminal_output}")    

    if directory_path:
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            append_to_prompt(f"Error: Invalid directory path: {directory_path}")
        else:
            directory_info = get_directory_structure_and_content(directory_path)
            append_to_prompt("Directory Structure and Contents:")
            append_to_prompt(f"Structure: {directory_info['structure']}")
            append_to_prompt(f"Contents: {directory_info['files']}")

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
        models = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash"
        ]
        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500