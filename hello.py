from flask import Flask
from flask import request
from flask import render_template
import subprocess,shlex,json,os,signal
from os import listdir
from os.path import isfile, join


app=Flask(__name__)

omxProcess=None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/youtube')
def youtube():
	return render_template('youtube.html')

@app.route('/pl',methods=["POST"])
def teste():
	global omxProcess
	os.system('killall omxplayer.bin')
	url=request.form['url']
	if url:
		cmdLine='omxplayyt "'+url+'"'
		args=shlex.split(cmdLine)
		omxProcess=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		return '{"status":true}'
	return '{"status":false}'

@app.route('/killprocc')
def killprocc():
	global omxProcess
	print omxProcess
	if omxProcess != None:
		print omxProcess.pid
		os.system('killall omxplayer.bin')
		omxProcess=None
		return '{"status":true}'
	return '{"status":false}'

@app.route('/command',methods=['POST'])
def message():
	comm=request.form['command']
	if comm:
		print comm
		return sendMsg(comm)
	return '{"status":false,"code":1}'


def sendMsg(msg):
	global omxProcess
	if omxProcess != None:
		try:
			omxProcess.stdin.write(msg)
			return '{"status":true}'
		except:
			return '{"status":false}'
	return '{"status":false}'

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
    si=s.replace(" ",'\\ ').replace("(","\(").replace(')','\)')
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
