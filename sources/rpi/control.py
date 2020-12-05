from datetime import datetime
import random
import math

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW
    GPIO_OKAY = True

except ModuleNotFoundError:
    GPIO_OKAY = False
    pass


class HydrogenSensor:
    # MQ-8 Hydrogen Sensor Parameters:
    H2Curve = [2.3, 0.93, -1.44]
    R0 = 10  # kOhm
    RL_VALUE = 10  # kOhm
    BASE_VOLTAGE = 5

    def __init__(self, ):

        if GPIO_OKAY:

            try:
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
                self.chan = AnalogIn(self.ads, ADS.P0)

                self.get_reading = self._get_readings

            except ValueError:
                print('connection to the i2c not successful')
                self.get_reading = self._fake_readings
        else:
            self.get_reading = self._fake_readings

    def _get_readings(self):
        return datetime.now(), self._convert_value(self.chan.voltage)

    def _fake_readings(self):
        return datetime.now(), random.randint(0, 100)

    def _convert_value(self, voltage):
        # from: http: // sandboxelectronics.com /?p = 196
        R = self.RL_VALUE * (self.BASE_VOLTAGE - voltage) / self.BASE_VOLTAGE
        ratio = R / self.R0
        return math.pow(10, ((math.log10(ratio) - self.H2Curve[1]) / self.H2Curve[2]) + self.H2Curve[0])


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
