#!/usr/bin/env bash

URL_regex='^(https?|ftp|file)'
XCPS='string:x-canonical-private-synchronous:SingleNotification'
# $XCPS is a notification option that keeps a single notification rather than a
# flood of many 
#(the SingleNotification part of it is a variable that doesn't # matter what
#it's called).
# It works by setting the SingleNotification as a title for all the
# notifications that "while read" get piped into it and allowing only a single
# notification window of the same name on screen.
pipedNotify() {
    while read PipedNotification; do
        notify-send -h "$XCPS" "$PipedNotification";
    done
}

case $1 in
    -p)
        pipedNotify ;;
    -s)
        # If $1 == -s && $2 ins't an empty string and is an URL by checking via
        # the regex operator =~ if all these tests pass $2 is sent to
        # send2playlist
        [[ -z $2 || ! $2 =~ $URL_regex ]] && exit 1

        notify-send -h "$XCPS" 'Sending to Playlist'

        send2playlist $2
        
        if [[ "$?" == "0" ]]; then
            notify-send -h "$XCPS" -u low 'Sent to Playlist'
        else
            notify-send -h "$XCPS" -u low 'Something went wrong'
        fi
esac
