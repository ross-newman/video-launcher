#!/bin/bash
# apt-get install libopencv-dev gstreamer1.0-plugins-bad

# Abaco Systems default settings (edit with care)
# Platform settings
export ARCH=$(arch)
# Gstreamer settings

export REMOTE_IP=127.0.0.1
#export REMOTE_IP=192.168.1.11 # Destination IP address for sending the RAW stream (For compression)
export HOST_IPADDR=192.168.1.107 # Our IP address for getting the stream back
export MULTICAST=239.192.1.114
#export MULTICAST=192.168.1.255
export UNICAST=${REMOTE_IP}
export PORT=5004 # IP Port number
export WIDTH=720
export HEIGHT=576
export RATE=30
export DEBUG_LEVEL=0
export GST_DEBUG=--gst-debug-level=$DEBUG_LEVEL
export OVERLAY_PLAYING="! textoverlay halignment=2 shaded-background=true text=\"Playing...\" "
export OVERLAY_RECORDING="! textoverlay halignment=2 shaded-background=true text=\"Recording...\" "
export ENCODING=$2
# Pan and Tilt head settings. -i to invert joystick, -s for scan mode if joystick is not working
export JOYSTICK_ARGS=-i
export RECORDING_HOME="$HOME/Videos/"
export SERIAL_PORT="/dev/ttyACM0"
#Visionworks settings
export VISIONWORKS_CAMERA="device://camera0"
# Encoder settings
export WEBCAM="/dev/video1"
export QUALITY_LEVEL=$5
export BITRATE=$6
export LOW_LATENCY=$7

# Done if no args were passed to us
case $4 in # Control Rate
disabled)
  export CONTROL_RATE=0
  ;;
variable)
  export CONTROL_RATE=1
  ;;
constant)
  export CONTROL_RATE=2
  ;;
variable-skip-frames)
  export CONTROL_RATE=3
  ;;
constant-skip-frames)
  export CONTROL_RATE=4
  ;;
*)
  export CONTROL_RATE=1
  ;;
esac

case ${10} in # Low Latency
disabled)
  export LOW_LATENCY=false
  ;;
disabled)
  export LOW_LATENCY=true
  ;;
esac

if [[ $# -ne 0 ]] ; then
  case "ts" in
    rtph264)
    export TRANSPORT_PAY=rtph264pay
    export TRANSPORT_DEPAY=rtph264depay
    ;;
    qt)
    export TRANSPORT_PAY=qtmux
    export TRANSPORT_DEPAY=qtdemux
    ;;
    ts)
    export TRANSPORT_PAY=mpegtsmux
    export TRANSPORT_DEPAY=tsdemux
    ;;
  esac

  if [ $3 == "multicast" ] 
  then
    export IPADDR=${MULTICAST}
    export MULTICAST_GROUP="address=${MULTICAST}"
  else
    export IPADDR=${UNICAST}
    export MULTICAST_GROUP="address=${IPADDR}"
  fi

#  echo "Detected ${ARCH} cpu..."
#  echo "Detected $2 transport..."
  case $ARCH in
  aarch64|arm)
    # Tegra X1 uses this
    export ENCODER_264=omxh264enc
    export DECODER_264=omxh264dec
    export ENCODER_265=omxh265enc
    export DECODER_265=omxh265dec
    export ARVIS_PATH=/opt/abaco/aravis/aarch64/
    export GST_BITRATE="bitrate"
    export SINK="nveglglessink -e"
    ;;
  armv7l)
    # Tegra K1 uses this
    export ENCODER_264=omxh264enc
    export DECODER_264=omxh264dec
    export ENCODER_265=x265enc # This doesnt exist yet
    export DECODER_265=x265dec # This doesnt exist yet
    export ARVIS_PATH=/opt/abaco/aravis/arm7l/
    export GST_BITRATE="target_bitrate"
    export SINK="xvimagesink"
    ;;
  *)
    # Use software codecs for all other platforms
    export ENCODER_264=x264enc
    export DECODER_264=x264dec # This doesnt exist yet
    export ENCODER_265=x265enc # This doesnt exist yet
    export DECODER_265=x265dec # This doesnt exist yet
    export ARVIS_PATH=/opt/abaco/aravis/x86_64/
    export GST_BITRATE="target_bitrate"
    export SINK="xvimagesink"
    ;;
  esac

  if [ $1 == "160x90" ] 
  then
    export WIDTH=160
    export HEIGHT=90
  fi

  if [ $1 == "160x120" ] 
  then
    export WIDTH=160
    export HEIGHT=120
  fi

  if [ $1 == "176x144" ] 
  then
    export WIDTH=176
    export HEIGHT=144
  fi

  if [ $1 == "320x180" ] 
  then
    export WIDTH=320
    export HEIGHT=180
  fi

  if [ $1 == "320x240" ] 
  then
    export WIDTH=320
    export HEIGHT=240
  fi

  if [ $1 == "352x288" ] 
  then
    export WIDTH=352
    export HEIGHT=288
  fi

  if [ $1 == "432x240" ] 
  then
    export WIDTH=432
    export HEIGHT=240
  fi

  if [ $1 == "640x360" ] 
  then
    export WIDTH=640
    export HEIGHT=360
  fi

  if [ $1 == "640x480" ] 
  then
    export WIDTH=640
    export HEIGHT=480
  fi

  if [ $1 == "800x448" ] 
  then
    export WIDTH=800
    export HEIGHT=448
  fi

  if [ $1 == "800x600" ] 
  then
    export WIDTH=800
    export HEIGHT=600
  fi

  if [ $1 == "864x480" ] 
  then
    export WIDTH=864
    export HEIGHT=480
  fi

  if [ $1 == "960x720" ] 
  then
    export WIDTH=960
    export HEIGHT=720
  fi

  if [ $1 == "1024x576" ] 
  then
    export WIDTH=1024
    export HEIGHT=576
  fi

  if [ $1 == "1280x720" ] 
  then
    export WIDTH=1280
    export HEIGHT=720
  fi

  if [ $1 == "1600x896" ] 
  then
    export WIDTH=1600
    export HEIGHT=896
  fi

  if [ $1 == "1920x1080" ] 
  then
    export WIDTH=1920
    export HEIGHT=1080
  fi
fi

