#   Copyright 2014 Michael Burget, Eric PTAK
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
This module provides a class for interfacing with HYTXXX sensors.
"""
from time import time, sleep
from myDevices.devices.i2c import I2C
from myDevices.utils.logger import info

class HYTXXX(I2C):
    """Class for interacting with an HYTXXX device."""
    VAL_RETRIES = 30
    
    def __init__(self, slave=0x28):
        """Initializes HYTXXX device.

        Arguments:
        slave: The slave address
        """
        I2C.__init__(self, int(slave))
        self.last_reading = 0        
        self.raw_temperature = None
        self.raw_humidity = None
        self.start_measuring()
    
    def start_measuring(self):
        """Start sensor measurement."""
        self.writeByte(0x0)
      
    def get_reading(self):
        """Gets the raw temperature and humidity readings from the sensor."""
        if self.last_reading + 2 < time():
            # Only take a new reading if a couple seconds have passed so if get_temperature and get_humidity
            # are called in succession they don't need to make two readings.
            self.start_measuring()
            for i in range(self.VAL_RETRIES):
                #C-code example from sensor manufacturer suggest to wait 100ms (Duration of the measurement)
                # no to get the very last measurement shouldn't be a problem -> wait 10ms
                # try a read every 10 ms for maximum VAL_RETRIES times
                sleep(.01)
                data_bytes = self.readBytes(4)
                stale_bit = (data_bytes[0] & 0b01000000) >> 6
                if (stale_bit == 0):
                    self.raw_temperature = ((data_bytes[2] << 8) | data_bytes[3]) >> 2
                    self.raw_humidity = ((data_bytes[0] & 0b00111111) << 8) | data_bytes[1]
                    self.last_reading = time()
                    return
            #Stale was never 0, so data are not actual
            raise Exception("HYT221(slave=0x%02X): data fetch timeout" % self.slave)
            
    def get_temperature(self):
        """Gets the temperature as a tuple with type and unit."""
        self.get_reading()
        if self.raw_temperature < 0x3FFF:
            temperature = self.set_precision((self.raw_temperature * 165.0 / 2**14) - 40.0)
            return (temperature, 'temp', 'c')
        else:
            raise ValueError("Temperature value out of range (RawValue=0x%04X Max:0x3FFF)" % raw_t)

    def get_humidity(self):
        """Gets the humidity as a tuple with type and unit."""
        self.get_reading()
        if self.raw_humidity < 0x3FFF:
            humidity = self.set_precision(self.raw_humidity * 100.0 / 2**14)
            return (humidity, 'rel_hum', 'p')
        else:
            raise ValueError("Humidity value out of range (RawValue=0x%04X Max:0x3FFF)" % raw_h)

    def set_precision(self, value):
        """Set the precision for a float."""
        return '{0:.2f}'.format(value)


class HYTXXXTest(HYTXXX):
    """Class for simulating an HYTXXX device."""

    def __init__(self):
        """Initializes the test class."""
        self.bytes = bytes([0x06, 0x66, 0x64, 0xDA])
        HYTXXX.__init__(self)

    def writeByte(self, data):
        """Write data byte."""
        pass

    def readBytes(self, size=1):
        """Read specified number of bytes."""
        return self.bytes[0:size]