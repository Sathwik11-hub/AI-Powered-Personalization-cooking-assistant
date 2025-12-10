from http.server import BaseHTTPRequestHandler
from streamlit.web import cli as stcli
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set the path to your Streamlit app
        sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
        sys.exit(stcli.main())
