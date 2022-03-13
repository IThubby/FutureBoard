#/bin/python

import audio
from time import sleep
from future import *
from machine import RTC
rtc = RTC()
from sugar import *
au = audio.Audio()
import ntptime
import time
import math
import random

x = 0



neopix=NeoPixel("P7",3)

neopix.setColorAll((0,0,0))
# Wifi Connect
wifi.connect(str("<ssid>"), "<pass>")
# Validate We're connected
if wifi.sta.isconnected():
  # If good, flash all the leds before setting the first to green
  neopix.setColorAll((0,255,0))
  neopix.update()
  neopix.setColorAll((0,0,0))
  sleep(0.3)
  neopix.setColorAll((0,0,255))
  neopix.update()
  neopix.setColorAll((0,0,0))
  sleep(0.3)
  neopix.setColorAll((0,255,0))
  neopix.update()
  sleep(0.3)
  neopix.setColorAll((0,0,0))
  sleep(0.2)
  neopix.setColor(0, (0, 175, 0))
  neopix.update()
  # Get the Time from ntp
  ntptime.settime(int(-8))
  screen.sync = 0
  while True:
    # Show date and time
    screen.fill((0, 0, 0))
    screen.text(str(str(str(rtc.datetime()[int(1)])+str("/"))+str(str(rtc.datetime()[int(2)])+str("/")))+str(rtc.datetime()[int(0)]),5,85,1,(255, 255, 0))
    screen.text(str(str(str(rtc.datetime()[int(4)])+str(":"))+str(str(rtc.datetime()[int(5)])+str(":")))+str(rtc.datetime()[int(6)]),5,98,1,(0, 170, 170))
    # Show IP address from wifi
    screen.text(str("IP: ")+str(wifi.sta.ifconfig()[0]),5,110,1,(255, 255, 255))
    # Show uptime in minutes
    screen.text(str("Up:")+str(round(time.ticks_ms() / 60000)),5,10,1,(0, 243, 255))
    # Temp - C to F
    screen.text(str("Tmp F:")+str(round(sensor.getTemp() * (9 / 5) + 32)),5,25,1,(255, 195, 255))
    # Light Sensor - ToDo: something useful
    screen.text(str("Lux:")+str(sensor.getLight()),5,40,1,(255, 255, 255))
    # Sound meter - may be good for audio reactivity later
    screen.text(str("Snd:")+str(au.loudness()),5,55,1,(56, 220, 255))
    # Compass using IMU heading
    screen.text(str("Head:")+str(sensor.heading()),5,70,1,(255, 0, 255))
    # Cardinal badges
    screen.text("N",117,33,1,(255, 0, 0))
    screen.text("S",117,90,1,(255, 0, 0))
    screen.text("E",144,61,1,(0, 119, 255))
    screen.text("W",88,61,1,(0, 119, 255))
    # The compass and its outline  
    screen.circle(120,65,20,(171, 183, 246),True)
    screen.circle(120,65,22,(255, 255, 0),False)
    # The needle - using degrees to coordinates, offset by -90 degrees.  Start at above circle center point
    # X=Cx+(radius*Math.cos((angle+(-90))*(Math.PI/180)));
    # Y=Cy+(radius*Math.sin((angle+(-90))*(Math.PI/180)));
    screen.line(120,65,120 + 20 * math.cos((sensor.heading() - 90) / 180.0 * math.pi),65 + 20 * math.sin((sensor.heading() - 90) / 180.0 * math.pi),(255, 0, 0))
    screen.refresh()
    # Random colors every second for the other 2 lights
    neopix.setColor(2, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
    neopix.setColor(1, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
    neopix.update()
    # Run a compass calibration if you press A - doesn't always work ... and after the screen has terrible refresh rates
    if sensor.btnValue('a'):
      calibrateCompass()
    else:
      sleep(1)
else:
  # If WiFi doesn't connect, set first LED to red and do nada
  neopix.setColor(0, (255, 0, 0))
  neopix.update()


