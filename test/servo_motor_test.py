#!/usr/bin/python# -*-coding: utf-8 -*-
# # Author : Original author WindVoiceVox
# # Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90
import RPi.GPIO as GPIO
import time
import sys 
class sg90:
  def __init__( self, pin, direction ): 
    GPIO.setmode( GPIO.BOARD )
    GPIO.setup( pin, GPIO.OUT )
    self.pin = int( pin )
    self.direction = int( direction )
    self.servo = GPIO.PWM( self.pin, 50 )
    self.servo.start(0.0)
  def cleanup( self ): 
    #Funktion zum Stoppen und GPIO Pins Freigeben
    self.servo.ChangeDutyCycle(self._henkan(0))
    time.sleep(0.3)
    self.servo.stop()
    GPIO.cleanup()
  def currentdirection( self ):
    return self.direction
  def _henkan( self, value ):
    return 0.05 * value + 7.0
  def setdirection( self, direction, speed ): #
    for d in range( self.direction, direction, int(speed) ):
      self.servo.ChangeDutyCycle( self._henkan( d )) 
      self.direction = d
      time.sleep(0.1)
    self.servo.ChangeDutyCycle( self._henkan( direction ) )
    self.direction = direction

servo = sg90(37,0)
servo.setdirection(100,10)
time.sleep(0.5)
servo.setdirection(-100,-10)
servo.cleanup()
print("Finsiasdfasdf")
