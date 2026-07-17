import sys
import os
import re
import tempfile
import uuid
import json
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy-load heavy modules only when needed
_cad_parser = None
_dfm_inspector = None
_report_generator = None

def get_cad_parser():
    global _cad_parser
    if _cad_parser is None:
        from src.cad_parser import CADParser
        _cad_parser = CADParser()
    return _cad_parser

def get_dfm_inspector():
    global _dfm_inspector
    if _dfm_inspector is None:
        from src.dfm_inspector import DFMInspector
        _dfm_inspector = DFMInspector()
    return _dfm_inspector

def get_report_generator():
    global _report_generator
    if _report_generator is None:
        from src.report_generator import ReportGenerator
        _report_generator = ReportGenerator()
    return _report_generator


@app.route('/')
def index():
    return render_template('index.html', processes={})

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        upload_id = str(uuid.uuid4())
        return jsonify({
            'upload_id': upload_id,
            'filename': filename,
            'filepath': filepath,
            'message': 'File uploaded successfully'
        }), 200
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        process = data.get('process', 'cnc_machining')
        
        parser = get_cad_parser()
        inspector = get_dfm_inspector()
        
        # Parse CAD file
        cad_data = parser.parse(filepath)
        
        # Run DFM analysis
        results = inspector.inspect(cad_data, process=process)
        
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
