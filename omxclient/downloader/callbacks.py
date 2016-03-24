
# Downloader mechanism for youtube
def downloadYoutube(self, body, outputdir):
    try:
        print "Downloading ", body
        os.system(dirc + " &&  youtube-dl "+body)
        print "Retrieving data from ", outputdir, " &&  youtube-dl ", body
    except Exception as e:
        print e

# Add here more resources downloaders, like vimeo, etc...
