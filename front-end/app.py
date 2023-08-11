import csv
import boto3
import subprocess
import pandas as pd

from flask import request
from flask import Flask, render_template, session
from trecs_backend import get_best_doctors


global trecs_df


# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templates', static_folder='static')

 
@app.route('/handle_click/<parameter>')
def handle_click(parameter):
    global trecs_df
    parameter=str(parameter)
    if 'Years' in parameter or 'Score' in parameter:
        result = trecs_df.sort_values(by=[parameter], ascending=False)
    else:
        result = trecs_df.sort_values(by=[parameter])
    return render_template('output.html',  tables=[result.to_html(classes='data')], titles=result.columns.values)



@app.route("/", methods=["GET", "POST"])
def home():
    global trecs_df
    if request.method == "POST":
        target_zipcode = request.form.get("zips")
        backend = get_best_doctors(target_zipcode)
        trecs_df = backend
        classes='table table-striped table-bordered tab-hover table-sm'
        return render_template('output.html',  tables=[backend.to_html(classes='data')], titles=backend.columns.values)

    else:
        return render_template("index.html")


if __name__=='__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
