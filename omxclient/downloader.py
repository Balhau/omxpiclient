import pika
import threading
import time
import os

"""
    This will download videos from youtube with the invocation of youtube-dl
"""
class YoutubeMQDownloader:
    cthread=None
    cchannel=None
    pchannel=None
    odir=None
    queue=None

    def __downloadURL(self,channel, method_frame, header_frame, body):
        dirc="cd "+self.odir
        try:
            print "Downloading ", body
            os.system(dirc + " &&  youtube-dl "+body)
            print "Retrieving data from ", self.odir, " &&  youtube-dl ", body
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            print e


    def __init__(self,rabbitMQHost,rabbitMQPort,q,directory):
        con = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost,rabbitMQPort))
        self.odir=directory
        self.queue=q
        self.pchannel=con.channel()
        self.cchannel=con.channel()
        self.pchannel.queue_declare(queue=self.queue)
        self.cchannel.basic_consume(self.__downloadURL, self.queue)
        self.cthread=threading.Thread(target=self.__consume)
        try:
            self.cthread.start()
        except KeyboardInterrupt:
            self.cthread.stop()


    def __consume(self):
        try:
            self.cchannel.start_consuming()
        except KeyboardInterrupt:
            self.cchannel.stop_consuming()

    def download(self,url):
        self.pchannel.basic_publish(exchange='',
                        routing_key=self.queue,
                        body=url)
        print " [x] Sent ", url
