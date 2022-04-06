import os

from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# App Configurations
UPLOAD_FOLDER = '/var/lib/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Instantiate App
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024  # Max size to 500kb
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{os.environ.get("POSTGRES_PASSWORD")}@db:5432/postgres'

# Instantiate DB
db = SQLAlchemy(app)

# Create PhotoModel Class
class Photo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  fpath = db.Column(db.String(80), unique=True, nullable=False)
  fname = db.Column(db.String(120), unique=True, nullable=False)
  fstatus = db.Column(db.String(80), unique=False, nullable=False)

  def __init__(self, filepath, filename, filestatus):
    self.fpath = filepath
    self.fname = filename
    self.fstatus = filestatus

# Create Requisite Table
db.create_all()

# Helper to check if file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper to check if file exists
def file_exists(filepath):
    return db.session.query(Photo).filter(Photo.fpath == filepath).first() is not None
    
# Convenience route to list files
@app.route("/list", methods=["GET"])
def list_uploads():
    uploads = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return {"all_files": uploads}

# Primary route   
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

        if file_exists(upload_path):
            response = {'message': 'This file already exists'}
            return make_response(response, 400)
        else:
            file.save(upload_path)

            new_file = Photo(upload_path, filename, 'QUEUED')
            db.session.add(new_file)
            db.session.commit()

            response = {'message': f"The file: {filename} was successfully uploaded"} 
            return make_response(response, 201)

if __name__ == "__main__":
    app.run(debug=True)