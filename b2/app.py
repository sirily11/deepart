import os

import sys
from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from werkzeug.utils import secure_filename
import json
from PIL import Image
from deepart import style_transform

SYSTEM_FOLDER = os.getcwd()
UPLOAD_FOLDER = 'uploaded/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = SYSTEM_FOLDER + "/static/" + UPLOAD_FOLDER
img_size = [300, 300]
selected_styles = []
'''
Main page
'''
@app.route('/')
def main():
    return render_template("hello.html")


'''
data for ComS 309
'''


@app.route('/data/', methods=['GET'])
def data():
    account = request.args.get('account')
    img = ["http://7108-presscdn-0-78.pagely.netdna-cdn.com/wp-content/uploads/2013/09/person-to-person-business.jpg",
           "http://i.dailymail.co.uk/i/pix/2017/04/11/06/3F23D80300000578-4399486-Palace_of_Westminster_view_from_the_Westminster_Bridge_One_of_th-a-12_1491890238800.jpg",
           "http://miriadna.com/desctopwalls/images/max/A-view-of-Rangitito-Island.jpg"]

    sumdict = [{"account_id": account, "first_name": "Qiwei", "last_name": "Li", "img_url": img[0]},
               {"account_id": account, "first_name": "Zikai", "last_name": "Luo", "img_url": img[1]},
               {"account_id": account, "first_name": "Json", "last_name": "Hacky", "img_url": img[2]}]
    return json.dumps(sumdict)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part

        if "start_generate" in request.form:
            print("Start")
            style_transform(saving_image_path='static/uploaded/generate_images',
                            content="static/" + view_all_images()[0],
                            style="static/" + view_all_style_images()[0])
            return "Waiting for transforming"

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
            filename = secure_filename(file.filename)
            savePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(savePath)
            img = Image.open(savePath)
            img.thumbnail(img_size)
            img.save(savePath)
            imglist = view_all_images()
            return render_template("picster_styles.html", has_uploaded=True,
                                   user_image=UPLOAD_FOLDER + filename,
                                   images=imglist,style_images = view_all_style_images())
    return render_template("picster_styles.html", has_uploaded=False,
                           style_images = view_all_style_images(),selected_style_imgs=selected_styles)



def view_all_images():
    imgList = os.listdir(app.config['UPLOAD_FOLDER'])
    newImgList = []
    for img in imgList:
        if allowed_file(img):
            newImgList.append(UPLOAD_FOLDER + img)
    return newImgList

def view_all_style_images():
    imgList = os.listdir('static/uploaded/style_images/')
    newImgList = []
    for img in imgList:
        if allowed_file(img):
            newImgList.append('uploaded/style_images/' + img)
    return newImgList

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)