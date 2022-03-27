#!/bin/bash

send2playlist $1

if [[ "$?" == "0" ]]; then
    notify-send -u low 'Sent to Playlist'
else
    notify-send -u low 'Something went wrong'
fi
