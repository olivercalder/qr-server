#!/usr/bin/sh

SERVICE_NAME="qr.service"

if [ "$(id -u)" -ne 0 ] ; then
    echo "Must be run as root"
    exit 0
fi

systemctl stop "$SERVICE_NAME"

rm "/etc/systemd/system/$SERVICE_NAME"
