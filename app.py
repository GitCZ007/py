#!/usr/bin/env python3
"""
A tiny Flask service that demonstrates:
* an HTTP endpoint
* reading configuration from the environment
* printing a friendly response
"""

from flask import Flask
import os
import time

app = Flask(__name__)

@app.route("/")
def hello():
    """Return a short greeting."""
    hostname = os.getenv("HOSTNAME", "unknown")
    greeting = os.getenv("GREETING", "Hello")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"{greeting}! You are running on <strong>{hostname}</strong> "
        f"at <strong>{current_time}</strong>"
    )


@app.route("/healthz")
def health():
    """Simple health‑check endpoint."""
    return "ok", 200


if __name__ == "__main__":
    # When run as a script, start the Flask dev server.
    # In a container we’ll use the Gunicorn‑style CMD in the Dockerfile.
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8080))
    app.run(host=host, port=port)
