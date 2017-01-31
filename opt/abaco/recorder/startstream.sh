#!/bin/bash
source /opt/abaco/recorder/global.sh $3 $4 $5 $7 $8 $9 ${10}

#export TARGET_BITRATE="target-bitrate" # K1
export TARGET_BITRATE="bitrate" # X1
export H264_PROFILE="! video/x-h264, profile=(string)high, level=(string)2 "

case $ARCH in
aarch64|arm)
  export X1_ENCODER="low-latency=${LOW_LATENCY} quality-level=${QUALITY_LEVEL} "
  ;;
*)
  export X1_ENCODER=""
  ;;
esac

case $1 in 
Webcam)
  export RATE=30 # camera only supports 30 so override global.sh
  export SOURCE="v4l2src device=${WEBCAM} do-timestamp=true io-mode=1 ! videoscale ! videoconvert "
;;
Synthetic)
  export SOURCE="videotestsrc pattern=$2 do-timestamp=true is-live=1 horizontal-speed=1"
;;
GigE)
  OFFSET_X=`expr 1920 - ${WIDTH}`
  OFFSET_X=`expr $OFFSET_X / 2`
  OFFSET_Y=`expr 1200 - ${HEIGHT}`
  OFFSET_Y=`expr $OFFSET_Y / 2`
echo $OFFSET_X $OFFSET_Y
  ${ARVIS_PATH}/arv-tool-0.4 control OffsetX=${OFFSET_X} OffsetY=${OFFSET_Y} Height=${HEIGHT} Width=${WIDTH} PixelFormat=BayerRG8 AcquisitionFrameRate=${RATE}
echo "  ${ARVIS_PATH}/arv-tool-0.4 control OffsetX=${OFFSET_X} OffsetY=${OFFSET_Y} Height=${HEIGHT} Width=${WIDTH} PixelFormat=BayerRG8 AcquisitionFrameRate=${RATE}"
  ${ARVIS_PATH}/arv-viewer &
  exit
;;
*)
  echo "ERROR unrecognised source element specificed $1"
;;
esac
 
echo "UDP streaming to ${IPADDR}..."
if [ $6 == "streaming" ]
then
  case $4 in 
  raw)
    echo "Starting RAW test stream...."
    gst-launch-1.0 -q ${SOURCE} ! "video/x-raw, width=${WIDTH}, height=${HEIGHT}, framerate=${RATE}/1, format=(string)UYVY" !  tee name=t ! queue ! rtpvrawpay ! udpsink host=${IPADDR} port=${PORT} t. ! xvimagesink sync=false $GST_DEBUG &
    echo "gst-launch-1.0 -q ${SOURCE} ! \"video/x-raw, width=${WIDTH}, height=${HEIGHT}, framerate=${RATE}/1, format=(string)UYVY\" !  tee name=t ! queue ! rtpvrawpay ! udpsink host=${IPADDR} port=${PORT} t. ! xvimagesink sync=false $GST_DEBUG"
    
    ;;
  h.264)
    echo "Starting H.264 test stream (${CONTROL_RATE})....."
echo "    gst-launch-1.0 -q ${SOURCE} ! \"video/x-raw, width=${WIDTH}, height=${HEIGHT}, format=(string)I420\" ! tee name=t ! ${ENCODER_264} ${GST_BITRATE}=${BITRATE} control-rate=${CONTROL_RATE} ${X1_ENCODER} ! ${TRANSPORT_PAY} ! udpsink host=${IPADDR} port=${PORT} t. ! xvimagesink sync=false $GST_DEBUG &"
    gst-launch-1.0 -q ${SOURCE} ! "video/x-raw, width=${WIDTH}, height=${HEIGHT}, format=(string)I420" ! tee name=t ! ${ENCODER_264} ${GST_BITRATE}=${BITRATE} control-rate=${CONTROL_RATE} ${X1_ENCODER} ! ${TRANSPORT_PAY} ! udpsink host=${IPADDR} port=${PORT} t. ! xvimagesink sync=false $GST_DEBUG &
    ;;
  h.265)
    echo "Starting H.265 test stream..."
    gst-launch-1.0 -q ${SOURCE} ! "video/x-raw, width=${WIDTH}, height=${HEIGHT}, format=(string)I420" ! tee name=t ! ${ENCODER_265} ${GST_BITRATE}=$BITRATE  ! udpsink host=${IPADDR} port=${PORT} t. ! xvimagesink sync=false $GST_DEBUG &
    ;;
  *)
  esac
else
  export filter=$6
  if [ $filter == "OpenCV::motioncells" ]
  then
    filter="motioncells gridx=32 gridy=32 "
  fi
  if [ $filter == "OpenCV::edgedetect" ]
  then
    filter="edgedetect"
  fi
  if [ $filter == "OpenCV::trackcolor" ]
  then
    /opt/abaco/recorder/track_camera &
    exit
  fi
  if [ $filter == "Visionworks::featuretrack" ]
  then
    /opt/abaco/visionworks/launch.sh $1 $filter $HEIGHT $WIDTH $VISIONWORKS_CAMERA
    exit
  fi
  if [ $filter == "Visionworks::houghlines" ]
  then
    /opt/abaco/visionworks/launch.sh $1 $filter $HEIGHT $WIDTH $VISIONWORKS_CAMERA
    exit
  fi


  echo "Starting >$filter<$6 test demo..."
#  gst-launch-1.0 -q ${SOURCE} ! "video/x-raw, width=${WIDTH}, height=${HEIGHT}, framerate=${RATE}/1, format=(string)UYVY" ! xvimagesink &
  gst-launch-1.0 -q ${SOURCE} ! "video/x-raw, width=${WIDTH}, height=${HEIGHT}, framerate=${RATE}/1, format=(string)UYVY" ! videoconvert ! $filter ! videoconvert ! xvimagesink $GST_DEBUG &
fi
