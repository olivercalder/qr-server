#!/usr/bin/sh

BIN_NAME="qr_server.py"
SERVICE_NAME="qr.service"
TEMPLATE_NAME="qr.service.template"
SERVER_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR_SED="$(echo "$SERVER_DIR" | sed 's/\//\\\//g')"

if [ "$(id -u)" -ne 0 ] ; then
    echo "Must be run as root"
    exit 0
fi

command -v qrencode > /dev/null && command -v python3 > /dev/null || {
    command -v apt && apt-get install -y qrencode python3
    command -v dnf && dnf install -y qrencode python3
    command -v yum && yum install -y qrencode python3
    command -v pacman && pacman -S qrencode python3
}

/usr/bin/env python3 -m pip list 2> /dev/null | grep -i flask > /dev/null ||
    /usr/bin/env python3 -m pip install flask

read -p "Input server hostname (i.e. localhost): " SERVER_HOSTNAME

read -p "Input server port (i.e. 5000): " SERVER_PORT

sed "s/SERVER_DIR/$SERVER_DIR_SED/g" "$TEMPLATE_NAME" |
    sed "s/SERVER_BIN/$BIN_NAME/g" |
    sed "s/SERVER_HOSTNAME/$SERVER_HOSTNAME/g" |
    sed "s/SERVER_PORT/$SERVER_PORT/g" |
    sed "s/SERVICE_NAME/$SERVICE_NAME/g" |
    tee "/etc/systemd/system/$SERVICE_NAME" > /dev/null

systemctl start "$SERVICE_NAME"

printf "Status of $SERVICE_NAME: "

systemctl is-active "$SERVICE_NAME"
