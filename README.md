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
