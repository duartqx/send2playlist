#Send2playlist
A python script that takes the url of a video streaming service as a parameter.
With this URL, the script uses requests.get and re.search to grab the URL's
page title. With the URL and title stored in memory, it writes both to a
playlist file. The titles on the playlist file serve the purpose of knowing at
first glance what videos are on the playlist. This script is used in
conjunction with pdlnmpv. pdlnmpv is a dmenu and bash script with options to
execute send2playlist, check the contents of the playlist, and start playing
the it with mpv, plus others.
