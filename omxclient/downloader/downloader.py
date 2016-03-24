import threading
import time
import os
from callbacks import *

"""
    This will download videos from youtube with the invocation of youtube-dl
"""

RESOURCE_CALLBACKS={
    'youtube' : downloadYoutube
}

class ResourceDownloader:

    def __init__(self,directory):
        self.session=Session()
        self.odir=directory
        self.queue=Queue()
        self.queue_thread=threading.Thread(target=self.__consume)
        self.__initialPopulate()
        try:
            self.cthread.start()
        except KeyboardInterrupt:
            self.cthread.stop()

    # This will fetch the pending requests that are stored in sqlite
    def __initialPopulate(self):



    def __consume(self):
        try:
            while True:
                request=self.queue.get()
                ##Get the proper callback and process the request url provided
                RESOURCE_CALLBACKS[request.service](request.url)
                self.session.delete(request)


        except KeyboardInterrupt:
            self.cchannel.stop_consuming()

    def putRequest(self,request):
        self.session.add(request)
        self.queue.put(request)

    def download(self,s,u):
        print " --> Request Received ", u
        request = DownloadRequest(service=s, url=u)
        self.putRequest(request)
