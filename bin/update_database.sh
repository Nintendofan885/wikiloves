#!/bin/bash
#
# Script to update the JSON database

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit

echo_time "Starting database update."

python database.py update

echo_time "Done with the update!"
