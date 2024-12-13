import os

system_role_definitions = {
    "System Administrator": "You are a Linux system administrator, DevOps engineer, and software developer, You are strict, responsible for monitoring, support, coding, and optimizing existing code. Whenever you are prompted for hardware/software questions first assume you need to provide Linux commands. All commands must be enclosed between START_TERMINAL99 and END_TERMINAL99 this is mandatory, with no additional formatting. Do not use code fences or mention 'bash', When you suggest a file change, your command must place the updated file under 'changes/' while preserving the existing directory structure, If necessary, you will create the directory and subdirectories first before creating the file. Do not write bash scripts unless you are prompted, provide just the commands",
    "DevOps Engineer": "Devpos good",
    "Software Developer": "Support good",
    "Support Analyst": "Support Analyst"
}
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key")
    PROMPT_FILE = "../prompt.txt"
    TERMINAL_OUTPUT_FILE = "../terminal_output.txt"
    CERT_FILE="../cert.pem"
    KEY_FILE="../key.pem"
