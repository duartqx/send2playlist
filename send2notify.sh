#!/usr/bin/env bash

URL_regex='^(https?|ftp|file)'
XCPS='string:x-canonical-private-synchronous:SingleNotification'
pipedNotify() {
    while read PipedNotification; do
        notify-send -h "$XCPS" "$PipedNotification";
    done
}

case $1 in
    -p)
        pipedNotify ;;
    *)
        [[ ! $1 =~ $URL_regex ]] && exit 1

        notify-send -h "$XCPS" 'Sending to Playlist'

        send2playlist $1
        
        if [[ "$?" == "0" ]]; then
            notify-send -h "$XCPS" -u low 'Sent to Playlist'
        else
            notify-send -h "$XCPS" -u low 'Something went wrong'
        fi
esac
