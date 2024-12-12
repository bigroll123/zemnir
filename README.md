
# **README: ChatGPT Command Execution Interface**

## **📘 Application Overview**

This application serves as a **prompt-based interface for OpenAI's ChatGPT API**. It allows users to interact with ChatGPT to generate responses, execute system commands on the host machine, and perform file-based interactions. Unlike a typical chatbot, this system is capable of **executing Linux commands on the host machine** and supports uploading files and folders for debugging purposes.

> ⚠️ **Warning:** Since ChatGPT is instructed to send Linux commands directly to the host terminal, be extremely cautious with the requests you make. Any command suggested by ChatGPT will be **executed on the host system**. Ensure proper validation and avoid unsafe commands.

---

## **💡 Key Features**

1. **Prompt-based Chat Interface**:
   - Users can send prompts directly to ChatGPT using the OpenAI API.
   - ChatGPT can provide **responses, suggestions, and code improvements**.

2. **Linux Command Execution**:
   - ChatGPT can **send Linux commands** directly to the host terminal.
   - Commands are executed automatically on the system and **command output is captured**.
   - **Command output can be sent back to ChatGPT** for debugging or further analysis.
   - All command execution logs are stored for auditing and debugging purposes.

3. **File Creation and Modification**:
   - ChatGPT can **create files on the host machine**.
   - File modifications are handled by creating new files, not overwriting existing ones.
   - **File updates are stored in the `changes/` directory** while maintaining the subdirectory structure of the files.

4. **File/Folder Uploads**:
   - Users can **upload files and folders** to the host machine.
   - These files can be sent to ChatGPT for **debugging, analysis, or improvement suggestions**.
   - Uploaded files are stored in a dedicated directory and can be used as part of the ChatGPT context.

---

## **📂 Directory Structure**

The application maintains a simple and logical file structure, as shown below.

```bash
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── static
│   │   └── styles.css
│   └── templates
│       └── index.html
├── config.py
├── README.md
├── requirements.txt
├── run.py
├── services
│   ├── chatgpt_service.py
│   ├── directory_processor.py
│   ├── file_manager.py
│   ├── __init__.py
│   └── terminal_runner.py
└── tests
    └── test_routes.py

```

### **Directory Explanations**

- **`changes/`**: This is where ChatGPT stores file updates. If ChatGPT suggests an improvement or code change, the new version is stored here. Subdirectory structures are preserved, so you can see exactly where files are updated.
- **`templates/`**: Contains the **HTML templates** used for the interface, like `index.html`.
- **`static/`**: Stores **CSS, JavaScript, and images** for the web interface.
  
---

## **⚙️ How It Works**

1. **User Input**:
   - The user provides a prompt in the web interface.
   - The user can also upload files, folders, or specific directories for ChatGPT to analyze.

2. **OpenAI API Request**:
   - The prompt is sent to **OpenAI's ChatGPT API**.
   - ChatGPT responds with suggestions, improvements, or commands to be executed.

3. **Command Execution**:
   - If ChatGPT suggests **Linux commands**, they are executed directly on the host system.
   - Command execution follows the format:
  
     ```bash
     START_TERMINAL99
     <command>
     END_TERMINAL99
     ```

   - The output of the command is captured and optionally sent back to ChatGPT for debugging.

4. **File Creation & Changes**:
   - If ChatGPT suggests **file changes**, they are created in the `changes/` directory.
   - The system maintains the **original file structure** and ensures no existing files are overwritten.
   - Files are created using this format:

     ```bash
     cat << EOF > changes/<path-to-file>
     <file-content>
     EOF
     ```

5. **File Uploads**:
   - Users can upload files or folders for debugging.

---

## **🔧 Configuration**

To configure the system, you may need to adjust the following variables:

| **Variable**         | **Description**                            | **Default**         |
|---------------------|---------------------------------------------|---------------------|
| `OPENAI_API_KEY`            | Your OpenAI API key                        | **Required**        |
| `PORT`               | The port to run the web server on          | **443** (HTTPS)     |
| `CERT_FILE`          | SSL certificate file for HTTPS             | `cert.pem`          |
| `KEY_FILE`           | Private key file for HTTPS                 | `key.pem`           |

---

## **⚠️ Important Warnings**

1. **Danger of Command Execution**:
   - ChatGPT can execute commands directly on the host machine. Be cautious when asking it to "delete files", "install software", or "run scripts".

2. **File System Changes**:
   - All files and updates are saved in the `changes/` directory to **prevent accidental overwriting of important system files**.

3. **Network Security**:
   - Use a firewall to restrict access to localhost.

---

## **🚀 How to Run**

1. **Generate ssl certificates and place them in the root folder**:

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout ../key.pem -out ../cert.pem -days 365 -nodes
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:

   ```bash
   export  OPENAI_API_KEY=sk-proj-87***
   python run.py
   ```

4. **Access the app**:
   - **<https://localhost>** (if SSL is enabled)  
   - **<http://localhost:5000>** (if SSL is disabled)

---

## **💡 Best Practices**

1. **Review Commands**: Always review the commands ChatGPT provides before executing them.
2. **Restrict Access**: Only allow trusted users to access the prompt.
3. **Backup Data**: Since ChatGPT can modify files, keep regular backups.
4. **Audit Logs**: Maintain logs of executed commands and uploaded files for audit purposes.

---

## **📞 Support**

If you have questions or need support, please contact the development team.

---

By following this documentation, you'll be able to securely and effectively manage **Linux command execution, file creation, and file uploads** using ChatGPT's intelligence. Stay safe, and happy debugging! 😊
