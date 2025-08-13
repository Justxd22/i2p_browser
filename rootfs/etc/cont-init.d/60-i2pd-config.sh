#!/bin/sh
#
# This script ensures a default i2pd.conf exists in the config volume.
#
set -e
set -u

I2PD_CONF_DIR="/config/i2pd"
I2PD_CONF_FILE="$I2PD_CONF_DIR/i2pd.conf"
I2PD_DEFAULT_CONF_FILE="/defaults/i2pd.conf"

# If a custom config already exists, do nothing.
if [ -f "$I2PD_CONF_FILE" ]; then
    echo "Custom i2pd.conf found, not overwriting."
    exit 0
fi

# Otherwise, copy the default configuration.
echo "No custom i2pd.conf found, creating default."
mkdir -p "$I2PD_CONF_DIR"
cp "$I2PD_DEFAULT_CONF_FILE" "$I2PD_CONF_FILE"

echo "Default i2pd.conf created at $I2PD_CONF_FILE"