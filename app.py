import sys
import traceback

# Diagnostic: try importing the app modules and catch errors
try:
    from flask import Flask, render_template, request, jsonify, send_file
    from werkzeug.utils import secure_filename
    import os
    import re
    import tempfile
    import uuid
    from collections import OrderedDict
    from datetime import datetime
    from pathlib import Path
    from typing import Dict, List

    # Try importing src modules
    from src.cad_parser import CADParser
    from src.dfm_inspector import DFMInspector
    from src.report_generator import ReportGenerator

    IMPORT_ERROR = None
except Exception as e:
    IMPORT_ERROR = traceback.format_exc()
    from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    if IMPORT_ERROR:
        return f'<h1>Import Error</h1><pre>{IMPORT_ERROR}</pre>', 500
    return render_template('index.html')

@app.route('/health')
def health():
    return 'OK', 200
