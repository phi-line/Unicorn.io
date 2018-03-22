from flask import Flask, render_template, request, flash, redirect, url_for, session
import os, sys
from os.path import abspath, dirname
from parse_pdf.parse import parse_resume
from rec_system.rec_system import rec_system
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/files/'
ALLOWED_EXTENSIONS = set(['pdf'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'static/files'
application.secret_key = 'youcantguessthisout'
SESSION_TYPE = 'redis' #use RedisSessionInterface
application.config.from_object(__name__)


@application.route('/', methods =['POST', 'GET'])
def home():
    if request.method == "POST":
        return redirect(url_for('start'))
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/start/', methods =['POST', 'GET'])
def start():
        if request.method == 'POST':
            size = int(request.form['size'])
            print('size', size)
            funding = request.form['funding']
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('start'))
            file = request.files['file']
            # if user does not selgitect file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                basedir = abspath(dirname(__file__))
                filepath = secure_filename(file.filename)
                path = os.path.join(basedir, application.config['UPLOAD_FOLDER'], filepath)
                file.save(path)

                user_keywords = parse_resume(path)
                rs = rec_system(size, funding, user_keywords)
                rs.loadCompaniesData()
                companyRankings = rs.rankCompaniesForUser()
                print("company rankings", companyRankings)

                return render_template('result.html', info=companyRankings)
        else:
            return render_template('start.html')


@application.route('/result/', methods =['POST', 'GET'])
def result(companyInfo):
    print(companyInfo)
    if request.method == "GET":
        return render_template('result.html', info = ['shit'])


if __name__ == '__main__':
  application.run('0.0.0.0', 9999, debug=True, use_reloader=False)
