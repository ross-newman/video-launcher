#!/bin/bash
export ARCH=$(arch)
echo "h2llo"
source /opt/abaco/recorder/global.sh
echo "hi"
echo "/opt/abaco/panandtilt/${ARCH}/joystick -d $SERIAL_PORT"
/opt/abaco/panandtilt/${ARCH}/joystick -d ${SERIAL_PORT} &
echo "Launched joystick process No $?"

