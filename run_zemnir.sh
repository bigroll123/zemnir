#!/bin/sh
export PYTHONPYCACHEPREFIX=/tmp/zemnir_pycache
mkdir -p $PYTHONPYCACHEPREFIX
# Confirming that the environment variable is set
echo "PYTHONPYCACHEPREFIX is set to $PYTHONPYCACHEPREFIX"
gunicorn --bind 0.0.0.0:8443 --certfile=cert.pem --keyfile=key.pem --timeout 120 app.main:app
