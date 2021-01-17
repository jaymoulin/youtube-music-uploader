#!/bin/sh

if [[ ! -f /root/oauth/oauth.key ]]; then
    trap 'exit 0' TERM INT
    while :
    do
        sleep 2
        /bin/true
    done
else
    trap 'kill -TERM $PID' TERM INT
    PARAMS=''
    if [[ "$REMOVE" == "1" ]] || [[ "$REMOVE" == "True" ]] || [[ "$REMOVE" == "true" ]] || [[ "$REMOVE" == "TRUE" ]]; then
        PARAMS="-r"
    fi
    if [[ "$ONESHOT" == "1" ]] || [[ "$ONESHOT" == "True" ]] || [[ "$ONESHOT" == "true" ]] || [[ "$ONESHOT" == "TRUE" ]]; then
        PARAMS="$PARAMS -o"
    fi
    if [[ "$LISTENER_ONLY" == "1" ]] || [[ "$LISTENER_ONLY" == "True" ]] || [[ "$LISTENER_ONLY" == "true" ]] || [[ "$LISTENER_ONLY" == "TRUE" ]]; then
        PARAMS="$PARAMS -l"
    fi
    if [[ "$DEDUP_API" ]]; then
        PARAMS="$PARAMS -w $DEDUP_API"
    fi
    youtube-music-upload -d /media/library -a /root/oauth/oauth.key $PARAMS &
    PID=$!
    wait $PID
    wait $PID
    EXIT_STATUS=$?
fi
