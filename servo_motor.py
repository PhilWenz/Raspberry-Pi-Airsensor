import RPi.GPIO as GPIO
import time
import sys


class Servo_Motor:
    def __init__(self, pin, direction):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = int(pin)
        self.direction = int(direction)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)

    def cleanup(self):
        # Funktion zum Stoppen und GPIO Pins Freigeben
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection(self):
        return self.direction

    def _henkan(self, value):
        return 0.05 * value + 7.0

    def setdirection(self, direction, speed):  #
        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction
        self.servo.ChangeDutyCycle(0)
