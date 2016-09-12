# dumpdr.py

This is a small script that provides the necessary `ffmpeg` commandline to download stuff from DR TV so that they can be watched offline. It still has a lot of rough edges, which honestly I don't know when or if I'll weed out. So far it picks the best possible quality and offers no support for subtitles. Pull requests welcome :)

## How to use it
Make a Python virtualenv, activate it and run `pip install -r requirements.txt`. Then you can invoke the program like this: `python dumpdr.py <link to dr.dk/tv program>`, e.g. `python dumpdr.py https://www.dr.dk/tv/se/tv-avisen-med-sporten/tv-avisen-med-sporten-og-vejret-2016-09-11`. 

The program outputs the command to issue in order to actually download the program. Obviously you'll need `ffmpeg` to dump the video.
