from flask import Blueprint, render_template, request, redirect, jsonify
from services.chatgpt_service import send_to_api
from services.file_manager import read_prompt, append_to_prompt, read_terminal_output
from services.chatgpt_service import send_directory_to_api
import os
from services.directory_processor import get_directory_structure_and_content

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/", methods=["GET"])
def index():
    current_prompt = read_prompt()
    terminal_output = read_terminal_output()
    return render_template(
        "index.html",
        current_prompt=current_prompt,
        terminal_output=terminal_output,
    )

@app_routes.route("/add_and_send", methods=["POST"])
def add_and_send():
    # Get the prompt text
    new_text = request.form.get("new_text", "").strip()
    # Get the directory path
    directory_path = request.form.get("directory_path", "").strip()

    # Append the user input to the prompt
    if new_text:
        append_to_prompt(f"User: {new_text}")

    # If a directory is provided, process it and append its structure and content
    if directory_path:
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            append_to_prompt(f"Error: Invalid directory path: {directory_path}")
        else:
            directory_info = get_directory_structure_and_content(directory_path)
            append_to_prompt("Directory Structure and Contents:")
            append_to_prompt(f"Structure: {directory_info['structure']}")
            append_to_prompt(f"Contents: {directory_info['files']}")

    # Send the prompt to the API
    send_to_api()
    return redirect("/")


@app_routes.route("/debug_directory", methods=["POST"])
def debug_directory():
    directory_path = request.json.get("directory_path")
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return jsonify({"error": "Invalid directory path"}), 400

    # Send directory data to API
    try:
        response = send_directory_to_api(directory_path)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


