echo_time() {
    echo "$(date +%F_%T) $*"
}

# Paths
: ${HOME_DIR:=/data/project/wikiloves}
: ${SOURCE_PATH:=$HOME_DIR/wikiloves}
