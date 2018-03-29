import json
import os
import threading

import time
from PIL import Image
from celery import Celery
from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from werkzeug.utils import secure_filename
from models.deepart import style_transform
from models.firebase import login_user_with_eamil
from models.firebase import signup_user_with_email

SYSTEM_FOLDER = os.getcwd()
UPLOAD_FOLDER = 'uploaded/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = SYSTEM_FOLDER + "/static/" + UPLOAD_FOLDER
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

img_size = [300, 300]
selected_styles = []

'''
Main page
'''
@app.route('/home')
def home():
    return render_template("home_page.html")


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

            thread = threading.Thread(target=style_transform, args=('static/uploaded/generate_images/{}.jpg'.format(time.time()),
                        "static/" + view_all_images()[0],
                        "static/" + view_all_style_images()[0] +"",2))
            thread.start()
            return "start processing"

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

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/signup')
def signup():
    if request.method == 'POST':
        email = request.form['login_email']
        password = request.form['login_password']
        message = signup_user_with_email(email,password)
        print(message)
        if message != False:
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template('login.html',message="Hello world")

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', transform_images=view_all_transform_images())


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['login_email']
        password = request.form['login_password']
        message = login_user_with_eamil(email,password)
        print(message)
        if message != False:
            return redirect("/home")
        else:
            return redirect("/login")
    return render_template("Login.html")


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

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
def view_all_transform_images():
    imgList = os.listdir('static/uploaded/transform_images/')
    newImgList = []
    for img in imgList:
        if allowed_file(img):
            newImgList.append('uploaded/transform_images/' + img)
    return newImgList

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
