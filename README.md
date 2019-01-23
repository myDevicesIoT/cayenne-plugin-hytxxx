# Cayenne HYTXXX Plugin
A plugin allowing the [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent) to read data from HYT221, HYT271, HYT939 and any other HYT sensors with the same interface and display it in the [Cayenne Dashboard](https://cayenne.mydevices.com).

## Requirements
### Hardware
* [Rasberry Pi](https://www.raspberrypi.org).
* An HYTXXX device, e.g. [HYT221](https://uk.farnell.com/ist-innovative-sensor-technology/hyt-221/sensor-humidity-digital-w-filter/dp/2191822)

### Software
* [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent). This can be installed from the [Cayenne Dashboard](https://cayenne.mydevices.com).
* [Git](https://git-scm.com/).

## Getting Started

### 1. Installation

   From the command line run the following commands to install this plugin.
   ```
   cd /etc/myDevices/plugins
   sudo git clone https://github.com/myDevicesIoT/cayenne-plugin-hytxxx.git
   ```
   
### 2. Restarting the agent

   Restart the agent so it can load the plugin.
   ```
   sudo service myDevices restart
   ```
   Temporary widgets for the plugin should now show up in the [Cayenne Dashboard](https://cayenne.mydevices.com). You can make them permanent by clicking the plus sign.

   NOTE: If the temporary widgets do not show up try refreshing the [Cayenne Dashboard](https://cayenne.mydevices.com) or restarting the agent again using `sudo service myDevices restart`.