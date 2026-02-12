#To be removed / obsolete
import os
import sys
sys.pycache_prefix = "/tmp/zemnir_pycache"
from config import Config

CERT_FILE = Config.CERT_FILE
KEY_FILE = Config.KEY_FILE


from app import create_app

app = create_app()

if __name__ == "__main__":
    # Check for SSL certificate files
    ssl_context = None
    cert_file = CERT_FILE
    key_file = KEY_FILE

    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)

    # Run the app
    app.run(host="0.0.0.0", port=8443, ssl_context=ssl_context, debug=True)

