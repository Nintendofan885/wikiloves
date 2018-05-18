echo_time() {
    echo "$(date +%F_%T) $*"
}

# Paths
: ${SOURCE_PATH:=$HOME/wikiloves}
: ${VIRTUAL_ENV_PATH:=$HOME/.venv}
