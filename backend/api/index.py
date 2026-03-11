from http.server import BaseHTTPRequestHandler
from streamlit.web import cli as stcli
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Resolve absolute path to the Streamlit app at project root
        app_path = os.path.join(os.path.dirname(__file__), "..", "..", "app.py")
        app_path = os.path.abspath(app_path)
        sys.argv = ["streamlit", "run", app_path, "--server.port=8501", "--server.headless=true"]
        sys.exit(stcli.main())
