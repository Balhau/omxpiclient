import threading
import signal
import time
from Queue import Queue
from callbacks import *
from sqlalchemy.orm import scoped_session
from dbase import session_factory,DownloadRequest

"""
    This will download videos from youtube with the invocation of youtube-dl
"""

RESOURCE_CALLBACKS={
    'youtube' : downloadYoutube
}

#This is a signal overriding for thread killing handling
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
    raise KeyboardInterrupt

Session=scoped_session(session_factory)

class ResourceDownloader:

    def __init__(self,directory):
        self.killer=GracefulKiller()
        self.output_directory=directory
        self.queue=Queue()
        self.queue_thread=threading.Thread(target=self.__consume)
        self.__initialPopulate()
        try:
            self.queue_thread.start()
        except KeyboardInterrupt:
            self.queue_thread.stop()
            raise

    # This will fetch the pending requests that are stored in sqlite
    def __initialPopulate(self):
        session=Session()
        for request in session.query(DownloadRequest).all():
            print "Added pending request: ", request.url
            self.queue.put(request)
        Session.remove()


    def __consume(self):
        empty=False
        request=None
        print self.killer.kill_now
        while self.killer.kill_now != True:
            try:
                s=Session()
                #Fetch request from the queue
                print "Fetching"
                try:
                    request=self.queue.get(timeout=1)
                    empty=False
                except:
                    empty=True
                if not empty:
                    print "Fetching: "
                    ##Get the proper callback and process the request url provided
                    RESOURCE_CALLBACKS[request.service](self.output_directory,request.url)
                    #Remove from the pending requests table
                    s.delete(request)
                    s.commit()
                    Session.remove()

            except KeyboardInterrupt:
                print "INTERRUPT 2"
                raise

    def putRequest(self,request):
        session=Session()
        session.add(request)
        session.commit()
        Session.remove()
        self.queue.put(request)

    def download(self,s,u):
        print " --> Request Received ", u
        request = DownloadRequest(service=s, url=u)
        self.putRequest(request)
