import csv
import boto3
import subprocess
import pandas as pd

from flask import request
from flask import Flask, render_template
from trecs_backend import get_best_doctors

# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templates', static_folder='static')
 


#rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('index.html')
 

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        target_zipcode = request.form.get("zips")
        print(target_zipcode)
        backend = get_data_doctors(target_zipcode)
        #print(backend)
        classes='table table-striped table-bordered tab-hover table-sm'
        return render_template('output.html',  tables=[backend.to_html(classes='data')], titles=backend.columns.values)


    return render_template("index.html")


if __name__=='__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
