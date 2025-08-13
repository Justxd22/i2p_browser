#!/bin/sh

set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error.

export HOME=/config

PIDS=

notify() {
    for N in $(ls /etc/logmonitor/targets.d/*/send)
    do
       "$N" "$1" "$2" "$3" &
       PIDS="$PIDS $!"
    done
}

# Verify support for membarrier.
if ! /usr/bin/membarrier_check 2>/dev/null; then
   notify "$APP_NAME requires the membarrier system call." "$APP_NAME is likely to crash because it requires the membarrier system call.  See the documentation of this Docker container to find out how this system call can be allowed." "WARNING"
fi

chown -R app:app /config/i2pd
echo "Starting i2pd daemon..."
/usr/sbin/i2pd --daemon --service --conf /config/i2pd/i2pd.conf --datadir /config/i2pd

echo "Launching loading screen..."
/usr/bin/loading_screen.py


# Wait for all PIDs to terminate.
set +e
for PID in "$PIDS"; do
   wait $PID
done
set -e

/usr/bin/firefox --version
exec /usr/bin/firefox "$@" >> /config/log/firefox/output.log 2>> /config/log/firefox/error.log

# vim:ft=sh:ts=4:sw=4:et:sts=4
