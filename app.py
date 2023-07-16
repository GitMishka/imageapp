from flask import Flask, request, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from PIL import Image as PilImage
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'uploads/'

class Image(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    mimetype = db.Column(db.String, nullable=False)

@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    filename = str(uuid.uuid4())
    
    img = PilImage.open(file)
    img.save(os.path.join(UPLOAD_FOLDER, filename + '.png'), 'PNG')

    new_image = Image(id=filename, filename=filename + '.png', mimetype='image/png')
    db.session.add(new_image)
    db.session.commit()
    return filename, 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    Image.query.filter_by(filename=filename + '.png').delete()
    db.session.commit()
    os.remove(os.path.join(UPLOAD_FOLDER, filename + '.png'))
    return '', 200


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    db.create_all()
    app.run(debug=True)
