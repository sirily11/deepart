import pyrebase
import json



user = None
def login_user_with_eamil(email,password):
    config = {
        "apiKey": "AIzaSyCHu2-6NyNWt1iQi3Z44UjhBOj3kIqk6QY",
        "authDomain": "vision-173113.firebaseapp.com",
        "databaseURL": "https://vision-173113.firebaseio.com",
        "projectId: ": "vision-173113",
        "storageBucket": "vision-173113.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email=email,password=password)
    except Exception as e:
        return False
    return user['idToken']



