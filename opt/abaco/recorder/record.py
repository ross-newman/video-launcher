#!/usr/bin/python
# -*- coding: utf-8 -*-

#sudo apt-get install python-imaging-tk gnuplot uuid-runtime

from Tkinter import *
from PIL import Image, ImageTk
from threading import Timer
import subprocess
import sys
import os
import signal
import tkFileDialog
import time
import platform
import os

global MB1
#MB1=1000000
MB1=1048576

class App:
  def __init__(self, master):
    # Timer Variables
    self.sec = 0
    self.var = IntVar()
    self.pan = IntVar()
    self.lowlat = IntVar()
    self.temp1 = IntVar()
    self.temp2 = IntVar()
    self.temp3 = IntVar()
    self.temp4 = IntVar()
    self.pattern = IntVar()
    self.res = StringVar()
    self.cam = StringVar()
    self.comp = StringVar()
    self.trans = StringVar()
    self.enclabel = StringVar()
    self.enclabel1 = StringVar()
    self.enclabel2 = StringVar()
    self.enclabel3 = StringVar()
    self.enclabel4 = StringVar()
    self.enclabel5 = StringVar()
    self.bandwidth = StringVar()
    self.mode = StringVar()
    self.controlrate = StringVar()
    self.qualitylevel = StringVar()
    self.brate = StringVar()
    self.arch=os.uname()[4]
    self.lowlat.set(0)
    self.temp1="--ºC "
    self.temp2="--ºC "
    self.bwtx="--MiB "
    self.bwrx="--MiB"
    self.homebase="/opt/abaco/"
    self.homedir="/opt/abaco/recorder/"
    self.res.set("640x480")
    self.cam.set("Synthetic")
    self.mode.set("streaming")   
    self.comp.set("raw")   
    self.trans.set("multicast")   
    if self.arch == "aarch64":
      self.enclabel.set("Settings below apply to the H.264 and H.265 OpenMax encoders:")   
    else:
      self.enclabel.set("Settings below apply to the H.264 OpenMax encoder:")       
    self.enclabel1.set("Control Rate")   
    self.enclabel2.set("Bitrate")   
    self.enclabel3.set("Low Latency")   
    self.enclabel4.set("Quality Level") 
    self.qualitylevel.set("0")
    self.controlrate.set("variable")
    self.brate.set("4000000")
    self.tempsfile = open(self.homedir + "temps.csv", 'w')
    self.tempsfile.write("Seconds,temp1,temp2,temp3,temp4\n")
    self.bwfile = open(self.homedir + "bw.csv", 'w')
    self.bwfile.write("Seconds,Rx,Tx\n")
    self.rxbw=0
    self.txbw=0
    self.samples = 0;
    self.temp= StringVar()
    height=2
    width=6
    fontsize=20
    frame=Frame(master, bd=0, relief=SUNKEN)
    frame1=Frame(bd=0, relief=SUNKEN)
    frame2=Frame(bd=0, relief=SUNKEN)
    frameencoder=Frame(bd=1, relief=SUNKEN)
    frame3=Frame(bd=0, relief=SUNKEN)
    frame4=Frame(bd=0, relief=SUNKEN)
    master.bind('t', self.test)
    master.bind('r', self.record)
    master.bind('p', self.play)
    master.bind('s', self.stop)
    master.bind('q', self.quitapp)
    self.intro = Label(frame, text="Abaco Systems - Video over Ethernet Demonstrator", font=("Helvetica", 16))
    self.intro.pack()
    self.help = Label(frame, text="Click Play/Record to capture live video or use 'Test' to generate a test source.\nRecordings will be stored in the local  directory in the format:\n    <UUID>-<ENCODING>-<HEIGH>x<WIDTH>.mkv\n\nFor support contact Abaco Systems (ross.newman@abaco.com).\n", justify=LEFT)
    self.help.pack()
    self.panandtilt = Checkbutton(frame1, text="Enable Pan and Tilt", variable=self.pan, command=self.togglepan)
    self.panandtilt.pack(side=RIGHT)
    frame.pack(padx=5, pady=5)
    frame1.pack(fill=X, padx=5, pady=5)
    frame2.pack(fill=X, padx=5, pady=5)
    frameencoder.pack(fill=X, padx=5, pady=5)
    frame3.pack(fill=X, padx=5, pady=5)
    self.showtemps = Button(frame1, 
                         text="Tempreture",
                         command=self.displaytemps)
    self.showtemps.pack(side=LEFT)
    self.temp.set(" " + self.temp1 + "ºC " + self.temp2 + "ºC")
    self.tempreture = Label(frame1, textvariable=self.temp)
    self.tempreture.pack(side=LEFT)
    self.showbw = Button(frame1, 
                         text="Bandwidth",
                         command=self.displaybw)
    self.showbw.pack(side=LEFT)
    self.bandwidth.set(" " + self.bwrx + "MiB " + self.bwtx + "MiB")
    self.bwlabel = Label(frame1, textvariable=self.bandwidth)
    self.bwlabel.pack(side=LEFT)
    self.record = Button(frame,
                         text="Record", fg="red",
                         command=self.record, height=height, width=width, font=("Helvetica", fontsize))
    self.record.pack(side=LEFT)
    self.play = Button(frame,
                         text="Play", fg="green",
                         command=self.play, height=height, width=width, font=("Helvetica", fontsize))
    self.play.pack(side=LEFT)
    self.stop = Button(frame,
                         text="Stop",
                         command=self.stop, height=height, width=width, font=("Helvetica", fontsize))
    self.stop.pack(side=LEFT)
    self.test = Button(frame,
                         text="Test",
                         command=self.test, height=height, width=width, font=("Helvetica", fontsize))
    self.test.pack(side=LEFT)
    self.qu = Button(frame3, 
                         text="Quit",
                         command=self.quitapp)
    self.qu.pack(side=RIGHT)
    self.recordings = Button(frame3, 
                         text="Recordings",
                         command=self.recordings)
    self.recordings.pack(side=RIGHT)
    self.editconf = Button(frame2, 
                         text="config",
                         command=self.editconfig)
    self.iconedit=PhotoImage(file=self.homedir + "configuration-editor.png")
    self.editconf.config(image=self.iconedit, width=20,height=20)
    self.editconf.pack(side=RIGHT)
#    self.webcam = Checkbutton(frame2, text="Webcam", variable=self.var)
    self.patternlabel = Label(frame2, text="Test pattern")
    self.patternlabel.pack(side=RIGHT)
    self.testpattern = Spinbox(frame2, from_=0, to=16, width=3)
    self.testpattern.pack(side=RIGHT)
    self.webcam = OptionMenu(frame2, self.cam, "Synthetic", "Webcam", "GigE")        
    self.webcam.pack(side=RIGHT)
    if self.arch == "aarch64":
      self.compression = OptionMenu(frame2, self.comp, "raw", "h.264", "h.265")
    else:
      self.compression = OptionMenu(frame2, self.comp, "raw", "h.264")
    self.compression.pack(side=RIGHT)
    self.transport = OptionMenu(frame2, self.trans, "multicast", "unicast")
    self.transport.pack(side=RIGHT)
    self.resolution = OptionMenu(frame2, self.res, "160x90", "160x120", "176x144", "320x180", "320x240", "352x288", "432x240", "640x360", "640x480", "800x448", "800x600", "864x480", "960x720", "1024x576", "1280x720", "1600x896", "1920x1080")
    self.resolution.pack(side=RIGHT)
    self.demomode = OptionMenu(frame2, self.mode, "streaming", "edgetv", "agingtv", "dicetv", "warptv", "radioactv", "rippletv", "optv", "OpenCV::motioncells", "OpenCV::edgedetect", "OpenCV::trackcolor", "Visionworks::featuretrack", "Visionworks::houghlines")
    self.demomode.pack(side=RIGHT)
    self.pattern = self.testpattern;

    frameenc1 = Frame(frameencoder)
    frameenc1.pack(fill=X)
    self.encodersettings = Label(frameenc1, textvariable=self.enclabel)
    self.encodersettings.pack(side=LEFT)

    frameenc2 = Frame(frameencoder)
    frameenc2.pack(fill=X)
    self.encodersettings1 = Label(frameenc2, textvariable=self.enclabel1, width=10)
    self.encodersettings1.pack(side=LEFT)
    self.control = OptionMenu(frameenc2, self.controlrate, "disabled", "variable", "constant", "variable-skip-frames", "constant-skip-frames")
    self.control.pack(side=LEFT)

    
    if self.arch == "aarch64":
      self.encodersettings3 = Label(frameenc2, textvariable=self.enclabel4, width=10)
      self.encodersettings3.pack(side=LEFT)
      self.quality = OptionMenu(frameenc2, self.qualitylevel, "0", "1", "2", "3")
      self.quality.pack(side=LEFT)

    self.encodersettings2 = Label(frameenc2, textvariable=self.enclabel2, width=7)
    self.encodersettings2.pack(side=LEFT)
    self.bitrate = Entry(frameenc2, textvariable=self.brate, width=10)
    self.bitrate.pack(side=LEFT, pady=5, padx=2) 

    if self.arch == "aarch64":
      self.lowlatency = Checkbutton(frameenc2, textvariable=self.enclabel3, width=10, variable=self.lowlat)
      self.lowlatency.pack(side=LEFT)

    # Abaco Logo
    self.iconPath = self.homedir + 'Abaco_transparent.png'
    self.icon = ImageTk.PhotoImage(Image.open(self.iconPath))
    self.icon_size = Label(frame3, image = self.icon)
    self.icon_size.pack(side=LEFT)
    # nVidia Logo
    self.iconPath2 = self.homedir + 'nvidia.png'
    self.icon2 = ImageTk.PhotoImage(Image.open(self.iconPath2))
    self.icon_size2 = Label(frame3, image = self.icon2)
    self.icon_size2.pack(side=LEFT)
    # OpenVX Logo
    self.iconPath3 = self.homedir + 'OpenVX.png'
    self.icon3 = ImageTk.PhotoImage(Image.open(self.iconPath3))
    self.icon_size3 = Label(frame3, image = self.icon3)
    self.icon_size3.pack(side=LEFT, padx=20)
    # OpenCV Logo
    self.iconPath4 = self.homedir + 'OpenCV.png'
    self.icon4 = ImageTk.PhotoImage(Image.open(self.iconPath4))
    self.icon_size4 = Label(frame3, image = self.icon4)
    self.icon_size4.pack(side=LEFT, padx=0)
    # Start temp update
    self.running=True
    self.timer = Timer(1, self.tick).start()
  def togglepan(self, event=0):
    if self.pan.get() == 1:
      print "Starting Pan and Tilt Head"
      self.rpro = subprocess.Popen([self.homebase + "panandtilt/launch.sh"])
    else:
      print "Stopping Pan and Tilt Head"
      subprocess.call(["pkill", "-1", "-f", "joystick"])    
  def test(self, event=0):
    subprocess.call([self.homedir + "startstream.sh", str(self.cam.get()), str(self.pattern.get()), str(self.res.get()), str(self.comp.get()), str(self.trans.get()), str(self.mode.get()), str(self.controlrate.get()), str(self.qualitylevel.get()), str(self.brate.get()), str(self.lowlat.get())])
  def recordings(self, event=0):
    fname=tkFileDialog.askopenfilename(filetypes=(("Matroska Video","*.mkv"), ("All files", "*.*")), initialdir="~/Videos", title="Open Recording")
    if fname:
      subprocess.call(["totem", fname])
  def record(self, event=0):
    self.rpro = subprocess.Popen([self.homedir + "recordstream.sh", str(self.res.get()), str(self.comp.get()), str(self.trans.get())])
  def play(self, event=0):
    print "Play video"
    self.ppro = subprocess.Popen([self.homedir + "playstream.sh", str(self.res.get()), str(self.comp.get()), str(self.trans.get())])
  def stop(self, event=0):
    print "Stop video"
    subprocess.call(["pkill", "gst-launch-1.0"])
    subprocess.call(["pkill", "gst-launch-0.10"])
    subprocess.call(["pkill", "track_camera"])
    subprocess.call(["pkill", "arv-viewer"])
    subprocess.call(["pkill", "-1", "-f", "nvx_demo_feature_tracker"])
    subprocess.call(["pkill", "-1", "-f", "nvx_demo_hough_transform"])
  def quitapp(self, event=0):
    print "Killing processes.."
    subprocess.call(["pkill", "gst-launch-1.0"])
    subprocess.call(["pkill", "gst-launch-0.10"])
    subprocess.call(["pkill", "track_camera"])
    subprocess.call(["pkill", "arv-viewer"])
    subprocess.call(["pkill", "-1", "-f", "nvx_demo_feature_tracker"])
    subprocess.call(["pkill", "-1", "-f", "nvx_demo_hough_transform"])    
    print "Quitting"
    self.running=False  
    root.quit()
  def displaytemps(self):
    self.tempsfile.close()
    # Create the graph
    # subprocess.call('cat temps.csv', shell=True)
    subprocess.Popen('gnuplot ' + self.homedir + 'temps.gph', shell=True)
    # Popup Window
    top = Toplevel()
    top.title("Temprerature Graph")
    msg = Label(top, text="Recorded tempreratures over the last %s seconds" %(self.samples))
    msg.pack(fill=BOTH)
    # Display the graph
    time.sleep(1)
    self.iconPath3 = self.homedir + 'temps.png'
    self.icon3 = ImageTk.PhotoImage(Image.open(self.iconPath3))
    self.icon_size3 = Label(top, image = self.icon3)
    self.icon_size3.pack()
    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()
    #open for append
    self.tempsfile = open(self.homedir + "temps.csv", 'a')
  def displaybw(self):
    self.bwfile.close()
    # Create the graph
    # subprocess.call('cat temps.csv', shell=True)
    if self.comp.get() != "raw":
      subprocess.Popen('gnuplot ' + self.homedir + 'bw-compress.gph', shell=True)
    else:
      subprocess.Popen('gnuplot ' + self.homedir + 'bw-raw.gph', shell=True)
    # Popup Window
    top = Toplevel()
    top.title("Network Bandwidth Graph")
    msg = Label(top, text="Recordedbandwidth over the last %s seconds" %(self.samples))
    msg.pack(fill=BOTH)
    # Display the graph
    time.sleep(1)
    self.iconPath4 = self.homedir + 'bw.png'
    self.icon4 = ImageTk.PhotoImage(Image.open(self.iconPath4))
    self.icon_size4 = Label(top, image = self.icon4)
    self.icon_size4.pack()
    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()
    #open for append
    self.bwfile = open(self.homedir + "bw.csv", 'a')
  def editconfig(self):
      subprocess.Popen('gedit ' + self.homedir + 'global.sh', shell=True)
  def tick(self):
    global MB1
    if platform.processor() != "x86_64":
      if self.running:
        file = open('/sys/class/thermal/thermal_zone0/temp', 'r')
        self.temp1 = file.readline()
        file.close()
        file = open('/sys/class/thermal/thermal_zone1/temp', 'r')
        self.temp2 = file.readline()
        file.close()
        file = open('/sys/class/thermal/thermal_zone2/temp', 'r')
        self.temp3 = file.readline()
        file.close()
        file = open('/sys/class/thermal/thermal_zone3/temp', 'r')
        self.temp4 = file.readline()
        file.close()
        self.samples += 1
        self.temp.set(" " + self.temp1[0:2] + "ºC " + self.temp2[0:2] + "ºC " + self.temp3[0:2] + "ºC " + self.temp4[0:2] + "ºC ")
        self.tempsfile.write(repr(self.samples) + "," + self.temp1[0:2] + "," + self.temp2[0:2] + "," + self.temp3[0:2] + "," + self.temp4[0:2])
        self.tempsfile.write("\n")
        # print self.temp.get()
        self.timer = Timer(1, self.tick).start()
        # Record bandwidth
        dev = open("/proc/net/dev", "r").readlines()
        header_line = dev[1]
        header_names = header_line[header_line.index("|")+1:].replace("|", " ").split()
        values={}
        for line in dev[2:]:
	        intf = line[:line.index(":")].strip()
	        values[intf] = [int(value) for value in line[line.index(":")+1:].split()]
	        if intf == "eth0" : 
	          if self.rxbw == 0:
	            self.rxbw=values[intf][0]
	            self.txbw=values[intf][8]  
	            return
	          self.bwrx = ((values[intf][0]-float(self.rxbw)) / MB1)
	          self.bwtx = ((values[intf][8]-float(self.txbw)) / MB1)
	          self.bandwidth.set(" " + str(str.format("{0:.2f}",self.bwrx)) + "MiB " + str(str.format("{0:.2f}",self.bwtx)) + "MiB")
	          self.bwfile.write(repr(self.samples) + "," + str.format("{0:.6f}",self.bwrx) + "," + str.format("{0:.6f}",self.bwtx) )
	          self.bwfile.write("\n")
	          self.rxbw=values[intf][0]
	          self.txbw=values[intf][8]

root = Tk()
root.title("Abaco Systems - Network Video Recorder")
root.geometry("680x460")
root.resizable(width=FALSE, height=FALSE)
app = App(root)
root.mainloop()
