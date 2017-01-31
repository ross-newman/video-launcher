#!/bin/bash
source /opt/abaco/recorder/global.sh  $1 $2 $3
export UUID=$(uuidgen)

echo "record $1 $2 $3"

case $2 in
  raw)
    echo "Recording RAW test stream (${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv)..."
    gst-launch-1.0 udpsrc port=${PORT} multicast-group=${IPADDR} caps="application/x-rtp, media=(string)video, encoding-name=(string)RAW, sampling=(string)YCbCr-4:2:2, depth=(string)8, width=(string)${WIDTH}, height=(string)${HEIGHT}, payload=(int)96, framerate=${RATE}/1" ! queue ! rtpvrawdepay ! tee name=t ! queue ! matroskamux ! filesink location=${RECORDING_HOME}${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv t. ! queue ${OVERLAY_RECORDING} ! xvimagesink &
    ;;
  h.264)
    echo "Recording H.264 test stream (${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv)..."
    gst-launch-1.0 udpsrc port=${PORT} ! ${TRANSPORT_DEPAY} ! queue ! tee name=t ! h264parse ! queue ! matroskamux ! filesink location=${RECORDING_HOME}${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv t. !  h264parse ! ${DECODER_264} ${OVERLAY_RECORDING} ! nveglglessink -e &
    ;;
  h.265)
    echo "Recording H.265 test stream (${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv)..."
# Not tested this pipeline!!!
    gst-launch-1.0 udpsrc port=${PORT} ! ${TRANSPORT_DEPAY} ! queue ! tee name=t ! h265parse ! queue ! matroskamux ! filesink location=${RECORDING_HOME}${UUID}-${ENCODING}-${HEIGHT}x${WIDTH}.mkv t. ! h265parse ! ${DECODER_264} ${OVERLAY_RECORDING} ! nveglglessink -e &
    ;;
  *)
    echo "Unrecognised format ${ENCODING}..."
    ;;
esac

