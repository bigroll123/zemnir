import os

def get_directory_structure_and_content(directory_path, exclude_items=None):
    """Traverse a directory and extract its structure and file contents."""
    if exclude_items is None:
        exclude_items = [".gitignore", ".vscode", ".git", "changes", "README.md", "LICENSE"]  # Default exclusions
        
    result = {"structure": {}, "files": {}}
    
    for root, dirs, files in os.walk(directory_path):
        # Filtering out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_items]
        # Capture directory structure
        relative_path = os.path.relpath(root, directory_path)
        if relative_path == ".": 
            relative_path = "/"
        result["structure"][relative_path] = dirs
        
        # Capture file contents, filtering excluded files
        for file in files:
            if file not in exclude_items:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        result["files"][os.path.relpath(file_path, directory_path)] = f.read()
                except Exception as e:
                    # Handle files that cannot be read
                    result["files"][os.path.relpath(file_path, directory_path)] = f"Error reading file: {e}"

    return result
