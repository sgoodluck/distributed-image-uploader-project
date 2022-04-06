import os, logging

from flask import Flask, flash, make_response, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/var/lib/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Instantiate App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024  # Max size to 500kb

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/list", methods=["GET"])
def list_uploads():
    uploads = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return {"all_files": uploads}
    
@app.route("/", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        response = {'message': 'You must upload a file'}
        return make_response(response, 400)

    file = request.files['file']
   
    if file.filename == '':
        response = {'message': 'Your filename must not be empty and be a proper filename'}
        return make_response(response, 400)

    if not allowed_file(file.filename):
        response = {'message': f"You may only upload files with the following types: {', '.join(ALLOWED_EXTENSIONS)}"}
        return make_response(response, 400)

    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        logging.debug("File Upload Successful - listing all files")
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            logging.debug(filename)

        response = {'message': f'The file {filename} was uploaded'}
        return make_response(response, 201)

if __name__ == "__main__":
    app.run(debug=True)