import os, socket

from flask import Flask, flash, request, redirect, url_for
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

# # Setup Home/Heartbeat Route TODO: Delete me before upload
# @app.route("/", methods=["GET"])
# def home():
#     return f"The server is alive! Container ID: {socket.gethostname()}"

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            dirs = os.listdir(app.config['UPLOAD_FOLDER'])

            print(upload_path)
            for file in dirs:
                print(file, flush=True)

            return redirect("/")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)