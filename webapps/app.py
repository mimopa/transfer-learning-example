#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This Application is used to classtify images using Tensorflow (InceptionV3) and build on Flask Framework.
import os, uuid
from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from image_rec import ImageRec 

# config - upload images filepath
UPLOAD_FOLDER = '/uploads'

app = Flask(__name__)
app.image_rec = ImageRec()

def is_image(filename):
    def _is_image(form, field):
        extensions = ['jpg', 'jpeg', 'png', 'gif']
        if filename and \
           filename.rsplit('.',1)[1] in extensions:
            raise ValidationError()
    return _is_image

def upload_file(file):
    # File Check
    if file and is_image(file.filename):
        file_name = str(uuid.uuid4()) +secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)
    return file_path

def image_recognition(file_path):
    labels = app.image_rec.run(file_path)
    return labels

# routing
@app.route('/', methods=['POST'])
def post():

    # file upload and image recognition
    file = request.files['file']
    if (file):
        file_path =upload_file(file)
        image_result = image_recognition(file_path)           
        return render_template('index.html',result=image_result,
                                file_path=file_path)
    return render_template('index.html')

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')
            
# routing imagefile
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# main http server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except Exception as ex:
        print(ex)
