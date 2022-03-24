# Send2playlist
![s2p](https://github.com/duartqx/images/blob/main/s2p.png?raw=true "s2p")
A Python script that takes the URL of a video streaming service as a parameter and uses requests.get and re.search to grab the URL's page title. It then writes title and URL to a playlist file. The titles on the playlist file serve the purpose of knowing at first glance what videos are on the playlist. This script is used in conjunction with pdlnmpv. pdlnmpv is a dmenu and bash script with options to execute send2playlist, check the contents of the playlist, and start playing it with mpv, plus others.

