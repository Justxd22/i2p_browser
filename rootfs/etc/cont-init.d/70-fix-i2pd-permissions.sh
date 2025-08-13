#!/bin/sh
#
# This script ensures the i2pd data directory has the correct ownership and
# permissions on every startup. This is critical for restarts when using a
# mounted volume. It runs as root during the init phase.
#
set -e
set -u

I2PD_DIR="/config/i2pd"

if [ -d "$I2PD_DIR" ]; then
    echo "Found i2pd data directory. Enforcing ownership and permissions..."
    # Set ownership to the 'app' user and group.
    chown -R app:app "$I2PD_DIR"
    # Set permissions: User gets full access, group gets read/execute, others get nothing.
    # This is a bit more open than i2pd's default but more reliable in Docker.
    chmod -R u=rwX,g=rX,o= "$I2PD_DIR"
fi

echo "i2pd permissions check complete."