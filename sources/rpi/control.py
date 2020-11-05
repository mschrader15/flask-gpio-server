from datetime import datetime
import random


class HydrogenSensor:
    def __init__(self, no_gpio=False):

        if not no_gpio:
            import board
            import busio
            import adafruit_ads1x15.ads1015 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn
            from datetime import datetime

            # Create the I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)

            # Create the ADC object using the I2C bus
            self.ads = ADS.ADS1015(self.i2c)
            self.ads.gain = 8

            # Create single-ended input on channel 0
            self.chan = AnalogIn(self.i2c, ADS.P0)

            self.get_reading = self._get_readings

        else:
            self.get_reading = self._fake_readings

    def _get_readings(self):
        return datetime.now(), self.chan.voltage

    def _fake_readings(self):
        return datetime.now(), random.randint(0, 100)

