# **README: Gemini Command Execution Interface**

## **📘 Application Overview**

This application serves as a **prompt-based interface for Google's Gemini API**. It allows users to interact with Gemini to generate responses, execute system commands on the host machine, and perform file-based interactions.

> ⚠️ **Warning:** Since Gemini is instructed to send Linux commands directly to the host terminal, be extremely cautious with the requests you make. Any command suggested by Gemini will be **executed on the host system**.

---

## **wrench Configuration**

To configure the system, you may need to adjust the following variables:

| **Variable** | **Description** | **Default** |
|---------------------|---------------------------------------------|---------------------|
| `GEMINI_API_KEY`    | Your Google Gemini API key                  | **Required** |
| `PORT`              | The port to run the web server on           | **443** (HTTPS)     |
| `CERT_FILE`         | SSL certificate file for HTTPS              | `cert.pem`          |
| `KEY_FILE`          | Private key file for HTTPS                  | `key.pem`           |

---

## **🚀 How to Run**

1. **Generate ssl certificates and place them in the root folder**:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout ../key.pem -out ../cert.pem -days 365 -nodespip install -r requirements.txt