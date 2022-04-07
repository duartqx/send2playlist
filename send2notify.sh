#!/usr/bin/env bash

URL_regex='^(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]\.[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]$'

[[ ! $1 =~ $URL_regex ]] && exit 1

send2playlist $1

if [[ "$?" == "0" ]]; then
    notify-send -u low 'Sent to Playlist'
else
    notify-send -u low 'Something went wrong'
fi
