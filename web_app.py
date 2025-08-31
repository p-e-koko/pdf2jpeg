#!/usr/bin/env python3
"""
Web interface for PDF to JPG Converter using Flask
"""

import os
import tempfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import zipfile
from pdf_to_jpg_converter import pdf_first_page_to_jpg, process_pdfs_bulk

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Clean up old uploaded and output files"""
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for file_path in Path(folder).glob('*'):
            try:
                if file_path.is_file():
                    os.remove(file_path)
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
            except:
                pass

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and conversion"""
    try:
        # Clean up old files first
        cleanup_old_files()
        
        # Check if files were uploaded
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        # Get conversion parameters
        dpi = int(request.form.get('dpi', 200))
        quality = int(request.form.get('quality', 95))
        scale_factor = float(request.form.get('scale_factor', 0.6))
        
        # Validate parameters
        if not (72 <= dpi <= 600):
            return jsonify({'error': 'DPI must be between 72 and 600'}), 400
        if not (1 <= quality <= 100):
            return jsonify({'error': 'Quality must be between 1 and 100'}), 400
        if not (0.1 <= scale_factor <= 2.0):
            return jsonify({'error': 'Scale factor must be between 0.1 and 2.0'}), 400
        
        # Save uploaded files
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                uploaded_files.append(file_path)
        
        if not uploaded_files:
            return jsonify({'error': 'No valid PDF files uploaded'}), 400
        
        # Convert files
        results = []
        converted_files = []
        
        for pdf_path in uploaded_files:
            success, original_path, result = pdf_first_page_to_jpg(
                pdf_path, 
                OUTPUT_FOLDER, 
                dpi=dpi, 
                quality=quality, 
                scale_factor=scale_factor
            )
            
            filename = Path(original_path).name
            if success:
                converted_files.append(result)
                results.append({
                    'filename': filename,
                    'status': 'success',
                    'output': Path(result).name
                })
            else:
                results.append({
                    'filename': filename,
                    'status': 'error',
                    'error': result
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'converted_count': len(converted_files),
            'total_count': len(uploaded_files)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a converted JPG file"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_all')
def download_all():
    """Download all converted files as a ZIP"""
    try:
        output_files = list(Path(OUTPUT_FOLDER).glob('*.jpg'))
        
        if not output_files:
            return jsonify({'error': 'No converted files available'}), 404
        
        # Create a temporary ZIP file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
                for file_path in output_files:
                    zip_file.write(file_path, file_path.name)
            
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name='converted_images.zip',
                mimetype='application/zip'
            )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear')
def clear_files():
    """Clear all uploaded and converted files"""
    try:
        cleanup_old_files()
        return jsonify({'success': True, 'message': 'All files cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting PDF to JPG Converter Web Interface...")
    print("Access the application at: http://localhost:5000")
    print("Network access: http://0.0.0.0:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=False, host='0.0.0.0', port=5000)
