import os
import uuid
import glob
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField
from wtforms.validators import DataRequired, ValidationError
import oauth1.authenticationutils as authenticationutils
from oauth1.oauth import OAuth

app = Flask(__name__)
UPLOAD_FOLDER = '.'
app.config['SECRET_KEY'] = '596b365c-7d23-4a5a-ac6a-633cc2427738'  # Replace with your actual secret key
app.config['UPLOAD_FOLDER'] = '.'

class FileExtensionValidator:
    def __init__(self, ext):
        self.ext = ext

    def __call__(self, form, field):
        if not field.data.filename.endswith(self.ext):
            raise ValidationError(f"File must end with '{self.ext}'")

class UploadForm(FlaskForm):
    file = FileField('Certificate', validators=[
        DataRequired(),
        FileExtensionValidator('.p12')
    ])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_files'))
    return render_template('upload.html', form=form)

@app.route('/files', methods=['GET'])
def uploaded_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.p12')]
    return render_template('files.html', files=files)

def generate_oauth_headers(consumer_key, signing_key, keystore_password, uri, http_verb, json_obj):
    signing_key = authenticationutils.load_signing_key(signing_key, keystore_password)
    authHeader = OAuth.get_authorization_header(uri, http_verb, json_obj, consumer_key, signing_key)
    headerdict = {'Authorization': authHeader}
    return headerdict

@app.route('/generate_oauth_headers', methods=['POST'])
def generate_headers():
    data = request.get_json()
    consumer_key = data.get('consumer_key')
    signing_key = data.get('signing_key')
    keystore_password = data.get('keystore_password')
    uri = data.get('uri')
    http_verb = data.get('http_verb')
    json_obj = data.get('json_obj')

    if all(param is not None for param in [consumer_key, signing_key, keystore_password, uri, http_verb, json_obj]):
        headers = generate_oauth_headers(consumer_key, signing_key, keystore_password, uri, http_verb, json_obj)
        return jsonify(headers)
    else:
        return jsonify({"error": "Missing required parameters"}), 400

@app.route('/api/upload_certificate', methods=['POST'])
def api_upload_certificate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File extension not allowed'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({'message': f'Successfully uploaded {filename}'}), 200

@app.route('/api/get_certificates', methods=['GET'])
def api_get_certificates():
    files = glob.glob(os.path.join(UPLOAD_FOLDER, '*.p12'))
    file_names = [os.path.basename(file) for file in files]
    return jsonify(file_names), 200

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
