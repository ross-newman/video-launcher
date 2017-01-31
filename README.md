![Abaco stripe](abaco/Abaco_background-1000x275.png)

# abaco-launcher
Python application launcher for gstreamer RTP pipelines.

# Project goals
- [x] Implement portable GUI gstreamer interface
- [x] Launcher for other Nvidia demos
- [x] Gstreamer streaming of RAW / H.264 / H.265 Ethernet streams
- [x] Enable Pololu servo controll of camer pan and tilt servos.
- [x] Gstreamer streaming of RAW / H.264 / H.265 Ethernet streams
- [x] TX1 & TK1 temperture sensing and logging
- [x] Transmit and receive Ethernet bandwidth logging

Some additional features that are planned.
- [ ] Parametrize launcher programs (read in demos from file).

# Installation
Install the dependancies:

    $ sudo apt-get install apt-get install python-imaging-tk gnuplot uuid-runtime
Clone the code:

    $ git clone https://github.com/ross-abaco/abaco-launcher
Run the Launcher without installing:

    $cd ./opt/abaco/launcher
    $ ./recorder.py
Installing the desktop shortcut:

    $ cd ./abaco-launcher
    $ make install
Once installed the launcher can be invoked from the desktop shortcut.
   
Uninstallation:

    $ make uninstall
## Screenshots
![Launcher screenshot](abaco/Abaco-launcher01.png)

Launcher running on TK1

![Temp sensing](abaco/Abaco-launcher02.png)

Temperture sensing on the TK1

# Links
* [Abaco Systems](http://abaco.com)
* [eLinux TX1](http://elinux.org/Jetson_TX1)
* [Nvidia devtalk](https://devtalk.nvidia.com/default/board/164/)
* [Abaco Systems MC10K1 - Tegra TK1 Mini COM Express module](https://www.abaco.com/products/mcom10-k1-mini-com-express)
* [Abaco Systems GRA113 - Maxwel GPGPU 3U VPX](https://www.abaco.com/products/gra113-graphics-board)

![Abaco stripe](abaco/Abaco Footer1000x100.png)
