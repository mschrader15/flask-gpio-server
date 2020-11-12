from datetime import datetime
import random

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW
    GPIO_OKAY = True

except ModuleNotFoundError:
    GPIO_OKAY = False
    pass


class HydrogenSensor:

    def __init__(self,):

        if GPIO_OKAY:
            import board
            import busio
            import adafruit_ads1x15.ads1015 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn

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


class SolenoidValve:

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.status = 'closed'
        if GPIO_OKAY:
            GPIO.setup(self.pin, GPIO.OUT)
        self.close()  # close the solenoid on initialization

    def close(self):
        if GPIO_OKAY:
            GPIO.output(self.pin, HIGH)
        self.status = 'closed'
        print('control level: valve has been closed')

    def open(self):
        if GPIO_OKAY:
            GPIO.output(self.pin, LOW)
        self.status = 'opened'
        print('control level: valve has been opened')

    def get_status(self):
        return self.name, self.status
