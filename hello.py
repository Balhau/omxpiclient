from flask import Flask
from flask import request
from flask import render_template
import os
import json
from os import listdir
from os.path import isfile, join


app=Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/killomx')
def kill_omxplayer():
	os.system('killall omxplayer.bin')
	return '{"status":"ok"}'

@app.route('/print',methods=['GET'])
def print_get():
	if request.args.get('ola',''):
		return "true"
	else:
		return "false"

def sh_quote(s):
    si=s.replace(" ",'\\ ')
    
    return si

@app.route('/play',methods=['POST'])
def print_post():
	file_path = request.form['file']
	dir_path = request.form['path']
	command='omxplayer '+sh_quote(dir_path)+sh_quote(file_path)+' -o local &'
	if file_path and dir_path:
		#print command
		os.system(command)
		return '{"status":"ok","command":"'+command+'"}'
	return '{"status":"error"}'

@app.route('/listdir',methods=['POST'])
def list_dir():
	extensions=['mp4','mkv','avi','flv']
	path=request.form['path']
	if path :
		jsData=[f for f in listdir(path) if f[-3:] in extensions]
		return json.dumps(jsData)

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')
