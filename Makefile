install:
	sudo cp -R ./opt/abaco /opt/.
	sudo mv /opt/abaco/Abaco.desktop ~/Desktop/.
	sudo mv /opt/abaco/recorder/AbacoSystems_icon.png ~/Pictures/.
	sudo chmod a+w /opt/abaco/recorder/*.csv
	sudo chmod a+w /opt/abaco/recorder/global.sh
	sudo chmod +x ~/Desktop/Abaco*
	sudo chown $(USER):$(USER) ~/Desktop/Abaco.desktop
	sudo apt-get -y install python-imaging-tk gnuplot uuid-runtime
	# =================================================================
	# Installation complete. Use the desktop icon to run the launcher.
	# =================================================================
	
clean:
	sudo rm -rf /opt/abaco
	sudo rm -f ~/Desktop/Abaco*
	rm -f ~/Pictures/AbacoSystems_icon.png

uninstall-apt:
	sudo apt-get -y remove python-imaging-tk gnuplot uuid-runtime
