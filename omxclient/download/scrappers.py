import os
"""
    This will download videos from youtube with the invocation of youtube-dl
"""
def downloadYoutube(outputdir,body):
    escaped_body=body.split("&")[0]
    dirc="cd "+outputdir
    try:
        print "Downloading ", escaped_body
        os.system(dirc + " &&  youtube-dl "+escaped_body)
        print "Retrieving data from ", outputdir, " &&  youtube-dl ", body
    except Exception as e:
        print e
