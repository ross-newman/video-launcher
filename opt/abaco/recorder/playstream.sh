#!/bin/bash
source /opt/abaco/recorder/global.sh $1 $2 $3

case $2 in 
  raw)
    echo "Playing RAW test stream..."
    gst-launch-1.0 udpsrc port=${PORT} caps="application/x-rtp, media=(string)video, encoding-name=(string)RAW, sampling=(string)YCbCr-4:2:2, depth=(string)8, width=(string)${WIDTH}, height=(string)${HEIGHT}, payload=(int)96, framerate=${RATE}/1" ! queue ! rtpvrawdepay ${OVERLAY_PLAYING} ! xvimagesink ${GST_DEBUG} &
  ;;
  h.264)
    echo "Playing H.264 test stream..."
    gst-launch-1.0 udpsrc port=${PORT} ${MULTICAST_GROUP} ! ${TRANSPORT_DEPAY} ! h264parse !  ${DECODER_264} ${OVERLAY_PLAYING} ! ${SINK} ${GST_DEBUG} & 
  ;;
  h.265)
    echo "Playing H.265 test stream (requires gstreamer 1.4)..."
    gst-launch-1.0 udpsrc port=${PORT} ${MULTICAST_GROUP}  ! queue ! ${TRANSPORT_DEPAY} !  ${DECODER_265} ${OVERLAY_PLAYING} ! ${SINK} ${GST_DEBUG} &
  ;;
  *)
    echo "Unknown stream type $2..."
  ;;
esac

