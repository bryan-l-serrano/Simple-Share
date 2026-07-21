from flask import Flask, request, send_from_directory, render_template
import os
import yaml
from datetime import datetime

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

UPLOAD_FOLDER = os.path.abspath(config['upload_folder'])
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/files', methods=['GET'])
def serve_files():
    path = request.args.get('path', '')
    if not path:
        files = []
        for f in os.listdir(UPLOAD_FOLDER):
            full_path = os.path.join(UPLOAD_FOLDER, f)
            stat = os.stat(full_path)
            files.append({
                'name': f,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            })
        return render_template('index.html', files=files)
    return send_from_directory(UPLOAD_FOLDER, path)

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        original_name = file.filename
        name, ext = os.path.splitext(original_name)
        new_filename = original_name
        counter = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
            new_filename = f"{name}_{counter}{ext}"
            counter += 1
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        return f'File {new_filename} uploaded successfully', 200
    return 'Invalid file', 400

@app.route('/files/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(full_path):
        os.remove(full_path)
        return f'File {filename} deleted successfully', 200
    return 'File not found', 404

if __name__ == '__main__':
    app.run(port=config['port'], debug=False)