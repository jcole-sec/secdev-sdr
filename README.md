### secdev-sdr
Software Defined Radio Scripts


#### Drivers - Linux

from repo:
```
sudo add-apt-repository ppa:ettusresearch/uhd
sudo apt-get update
sudo apt-get install libuhd-dev uhd-host
ref: USRP Hardware Driver and USRP Manual: Binary Installation 
```
 

USB udev rules

```
cd <install-path>/lib/uhd/utils
sudo cp uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
``` 

- [USRP Hardware Driver and USRP Manual: Transport Notes](https://files.ettus.com/manual/page_install.html)


GNU radio source reference: [USRP Source - GNU Radio](https://wiki.gnuradio.org/index.php?title=USRP_Source)

NI - [NI-USRP Download](https://www.ni.com/en-us/support/downloads/drivers/download.ni-usrp.html#437034) 

  

#### Training

- [SDR Academy](https://www.ettus.com/support/sdr-academy/)
- [Tutorials - GNU Radio](https://wiki.gnuradio.org/index.php?title=Tutorials#GNU_Radio_Academy)

 

FM tutorial - [How To Build an FM Receiver with the USRP in Less Than 10 Minutes](https://www.youtube.com/watch?v=KWeY2yqwVA0)
- grc file: https://files.ettus.com/app_notes/fm_rcvr/fm_example.grc
