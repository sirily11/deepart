from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("hello.html")


@app.route('/api/', methods=['GET'])
def getQ():
    userid = request.args.get('userid')
    name = request.args.get('name')
    age = request.args.get('age')
    sumdict = {"user_id": userid, "name": name, "age": age}

    return json.dumps(sumdict)
