#PIOmxControl

This is a web interface for RaspberryPI and omxplayer. This enable a device with a web browser
to search for movies, to play and stop. This is a very elementary tool but it is the bare minimum to
control the movies with your smartphone

Next steps:

* Fix design
* Add controllers

##Software needed

This front end application use on back end some utility programs you need to install first to successfully run this program. They are needed, for example, to render video on raspberry, parse and download media stream from public endpoints and to play and stop stream of audio (for example for the radio mechanism). 
Without further add here are the programs:

* omxplayer: Program to render video
* youtube-dl: Program to parse media endpoints and retrieve video stream
* mpd: Daemon to reproduce audio
* mpc: Utility to parse and reproduce endpoints

# Future developments

The next milestone is all about live tv. Know the time is about find and reverse RTMP endpoints and store it on the server. When a significantly number of endpoints is stored and working we will proced to the development of front end views and python controllers to able the Pi to play those live stream videos. Yes we could develop this in parallel, however I think it's preferable going by baby steps. 

Don't worry, be happy
