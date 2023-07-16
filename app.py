from flask import Flask, request, send_file
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    filename = str(uuid.uuid4())
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename, 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)

