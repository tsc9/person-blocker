from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import time
import datetime
import json
import math
import base64
import os
import subprocess
import random
import string

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


@app.route('/personBlocker/<string:s>')
def personBlocker(s):
    
    return "%s"%(s)

#網頁執行/say_hello時，會導至index.html
@app.route('/say_hello/',methods=['GET'])
def getdata():
    return render_template('index.html')

#index.html按下submit時，會取得前端傳來的username，並回傳"Hellold! "+name
@app.route('/say_hello',methods=['POST'])
def submit():
    name = request.form.get('username')
    return ("Hello, "+name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    imgSrc = ""

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            cmd_str = 'rm -rf static/*'
            subprocess.call(cmd_str, shell=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            objectName = request.form.get('objectName').lower()
            if(objectName==""):
                cmd_str = 'python person_blocker.py -i static/' + filename
                subprocess.call(cmd_str, shell=True)
            elif (objectName=="label"):
                cmd_str = 'python person_blocker.py -i static/' + filename + ' -l'
                subprocess.call(cmd_str, shell=True)
            elif(is_number(objectName)):
                cmd_str = 'python person_blocker.py -i static/' + filename + ' -o ' + objectName
                subprocess.call(cmd_str, shell=True)
            else:
                cmd_str = 'python person_blocker.py -i static/' + filename + ' -o \'' + objectName + '\''
                subprocess.call(cmd_str, shell=True)


            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            cmd_str = 'mv static/person_blocked.png static/pb' + filename.rsplit('.', 1)[0] +ran_str+'.png'
            subprocess.call(cmd_str, shell=True)
            imgSrc = "static/pb"+filename.rsplit('.', 1)[0]+ran_str+ ".png"

            return render_template("service.html",imgSrc = imgSrc)
            
    return render_template("service.html",imgSrc = imgSrc)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 9489, debug=True)

