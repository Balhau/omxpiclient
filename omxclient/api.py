def buildAPI(hostname):
    API = {
        'downloadPatterns' : [
            {
                'pattern':'https://www.youtube.com/watch?',
                'poster': 'http://'+hostname+'/youtube/downloader'
            }
        ],
        'api' : {
            'start_torrents' : 'http://'+hostname+'/starttorrents',
            'stop_torrents' : 'http://'+hostname+'/stoptorrents'
        }
    }
    return API;
