#!/bin/bash
#
# Script to update the JSON database

echo_time() {
    echo "$(date +%F_%T) $*"
}

cd ~/wikiloves || exit

echo_time "Starting database update."

python database.py update

echo_time "Done with the update!"
