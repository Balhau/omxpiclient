import os
"""
    This will download videos from youtube with the invocation of youtube-dl
"""
def downloadYoutube(outputdir,body):
    dirc="cd "+outputdir
    try:
        print "Downloading ", body
        os.system(dirc + " &&  youtube-dl "+body)
        print "Retrieving data from ", outputdir, " &&  youtube-dl ", body
    except Exception as e:
        print e
