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
            'stop_torrents' : 'http://'+hostname+'/stoptorrents',
            'list_downloads' : 'http://'+hostname+'/list/downloads/pending'
        }
    }
    return API;
