#!/usr/bin/env bash

USER_ID="${USER_ID:-1000}"

# variables
OUT_DIR="${OUT_DIR:-/appimages}"
NETWORK="${NETWORK:-regtest}"
APP_NAME=""
PORT_NAME=""
PORT_OPT=()
APP_NAME_SUFFIX_OPT=()
if [ -n "$LN_PORT" ]; then
    PORT_NAME="-$LN_PORT"
    PORT_OPT=("--ldk-port=$LN_PORT")
fi

if [ -n "$APP_NAME_SUFFIX" ]; then
    APP_NAME="-$APP_NAME_SUFFIX"
    APP_NAME_SUFFIX_OPT=("--app-name=$APP_NAME_SUFFIX")
fi

# compile resources
poetry run pyside6-rcc src/resources.qrc -o src/resources_rc.py

# build appimage
poetry run build-iris-wallet \
    --distribution=appimage \
    --network="$NETWORK" \
    "${APP_NAME_SUFFIX_OPT[@]}" \
    "${PORT_OPT[@]}"

# copy appimage to /appimage (assumed to be mounted from the host)
if ! [ -d "$OUT_DIR" ]; then
    echo "ERR: output directory $OUT_DIR not found"
    exit 1
fi
cp iriswallet* "$OUT_DIR/iriswallet${APP_NAME}-$NETWORK$PORT_NAME.AppImage"
chown -R "$USER_ID:$USER_ID" "$OUT_DIR"
