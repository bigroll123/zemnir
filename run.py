from app import create_app
import os
import sys

sys.pycache_prefix = '/tmp/zemnir_pycache'

app = create_app()

if __name__ == "__main__":
    # Check for SSL certificate files
    ssl_context = None
    cert_file = "../cert.pem"
    key_file = "../key.pem"

    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)

    # Run the app
    app.run(host="0.0.0.0", port=8443, ssl_context=ssl_context, debug=True)

