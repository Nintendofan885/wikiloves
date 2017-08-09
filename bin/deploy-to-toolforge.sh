#!/bin/bash
user="";
if [ -n "$1" ]; then
  user="$1"@
fi
ssh "$user"tools-dev.wmflabs.org <<'ENDSSH'
become wikiloves
cd wikiloves
git pull
git log @{1}.. --oneline --reverse -C --no-merges
echo "Deploy done."
echo "Please update the Server Admin Log via IRC:"
echo "https://webchat.freenode.net/?channels=#wikimedia-labs"
ENDSSH
