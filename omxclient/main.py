from flask import Flask
from flask import request
from flask import render_template
import subprocess,shlex,json,os,signal
from download.downloader import *
from os import listdir
from os.path import isfile, join
from radio import *
from utils import *
from api import buildAPI


outputdir="/media/BalhauWD/MediaLibrary/downloads"
#outputdir="/tmp/"
torrentsStartCommand='/home/pi/starttorrent.sh'

rd=ResourceDownloader(outputdir)

app=Flask(__name__)

omxProcess=None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/youtube')
def youtube():
	return render_template('youtube.html')

@app.route('/torrents')
def torrents():
	return render_template('torrents.html')

@app.route('/messages')
def messages():
	return render_template('messages.html')


@app.route("/youtube/downloader",methods=["POST"])
@crossdomain(origin='*')
def youtubeDownload():
	print "ENTROU"
	url=request.form['url']
	rd.download('youtube',url)
	return "OK"

@app.route("/api/description",methods=["GET"])
@crossdomain(origin='*')
def apiDescription():
	host=None
	try:
		host=request.headers['X-Forwarded-Host']
	except:
		host=request.headers['host']
	return json.dumps(buildAPI(host))

@app.route("/downloader")
def downloader():
	return render_template('downloader.html')

@app.route("/youtubev3/search",methods=["POST"])
def youtubeSearch():
	url=request.form['url']
	return "YES: "+url

@app.route('/starttorrents')
@crossdomain(origin='*')
def starttorrents():
	#then run the start script
	#first stop the deamon if it is enabled
	os.system('killall -9 transmission-daemon')
	os.system(torrentsStartCommand)
	return "{status:true}"

@app.route('/stoptorrents')
@crossdomain(origin='*')
def stoptorrents():
	#just kill the transmission daemon
	os.system('killall -9 transmission-daemon')
	return "{status:true}"

@app.route('/pl',methods=["POST"])
def teste():
	global omxProcess
	os.system('killall omxplayer.bin')
	os.system('killall youtube-dl')
	url=request.form['url']
	print "Play: "+url
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
    si=s.replace(" ",'\\ ').replace("(","\(").replace(')','\)').replace("'","\\'")
    print si
    return si

@app.route('/play',methods=['POST'])
def print_post():
	global omxProcess
	file_path = request.form['file']
	dir_path = request.form['path']
	os.system('killall omxplayer.bin')
	command='omxplayer '+sh_quote(dir_path)+sh_quote(file_path)+' -o local &'
	if file_path and dir_path:
		#print command
		args=shlex.split(command)
		omxProcess=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		return '{"status":"ok","command":"'+command+'"}'
	return '{"status":"error"}'

@app.route('/listdir',methods=['POST'])
def list_dir():
	extensions=['mp4','mkv','avi','flv','mp3','mov']
	path=request.form['path']
	if path :
		jsData=[f for f in listdir(path) if f[-3:] in extensions or os.path.isdir(os.path.join(path,f))]
		jsData.append("../")
		return json.dumps(jsData)


@app.route('/radio',methods=['GET'])
def radio():
	return render_template('radio.html')


@app.route('/local',methods=['GET'])
def local():
	return render_template('local.html')


@app.route('/radiocountries',methods=['GET'])
def getradiocountries():
	r=RadioService()
	countries=r.getCountries()
	nlist=[]
	for country in countries:
		aux={}
		aux["link"]=country.attrib['href']
		aux["name"]=country.text_content()
		nlist.append(aux)
	return json.dumps(nlist)

@app.route('/countryradios',methods=['POST'])
def getradiocountry():
	country=request.form['country']
	r=RadioService()
	radios=r.getCountryRadio(country)
	r=radios[0]
	e=radios[1]
	nlist=[]
	pos=0
	for radio in r:
		aux={}
		aux["link"]=radio.attrib['href']
		aux["name"]=radio.text_content()
		aux["endpoints"]=[]
		for endp in e[pos]:
				aux2={}
				aux2["link"]=endp.attrib['href']
				aux2["name"]=endp.text_content()
				aux["endpoints"].append(aux2)
		nlist.append(aux)
		pos=pos+1
	return json.dumps(nlist)

@app.route('/playradio',methods=['POST'])
def playRadio():
	radioStation=request.form['radio']
	r=RadioService()
	r.playRadio(radioStation)
	return '{"status":true}'

@app.route("/ping",methods={'GET'})
def ping():
	f=open('ipping.txt','a')
	ipclient=""
	h = request.headers
        for header, value in request.headers.items():
		if(header == 'X-Forwarded-For'):
			ipclient=value

	f.write("{'host': '"+request.args.get('host')+"',")
	f.write("'ip': '"+ipclient+"'}")
	f.write("\n")
	f.close()
	return '{"status":true}'


@app.route('/stopradio',methods=['GET'])
def stopRadio():
	r=RadioService()
	r.stopRadio()
	return '{"status":true}'

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0',use_reloader=False)
