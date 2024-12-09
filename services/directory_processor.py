import os

def get_directory_structure_and_content(directory_path):
    """
    Traverse a directory and extract its structure and file contents.
    """
    result = {"structure": {}, "files": {}}

    for root, dirs, files in os.walk(directory_path):
        # Capture directory structure
        relative_path = os.path.relpath(root, directory_path)
        if relative_path == ".":
            relative_path = "/"
        result["structure"][relative_path] = dirs

        # Capture file contents
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    result["files"][os.path.relpath(file_path, directory_path)] = f.read()
            except Exception as e:
                # Handle files that cannot be read
                result["files"][os.path.relpath(file_path, directory_path)] = f"Error reading file: {e}"

    return result
