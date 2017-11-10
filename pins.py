import RPi.GPIO as GPIO
from time import sleep

POLL_RATE = 0.25

RED = 2
GREEN = 3
ORANGE = 4

colors = [RED, GREEN, ORANGE]

ports = [14, 15, 18]
colorNames = {2: 'red', 3: 'green', 4: 'orange'}

plugs = [None, None, None]

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(ORANGE, GPIO.OUT)

for port in ports:
  GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def checkColor(color):
  GPIO.output(RED, 0)
  GPIO.output(GREEN, 0)
  GPIO.output(ORANGE, 0)
  GPIO.output(color, 1)
  for port in ports:
    portPos = ports.index(port)
    if GPIO.input(port):
      return portPos
    else:
      return None

try:
  while True:
    for color in colors:
      colorPin = checkColor(color)
      if colorPin != None:
        if plugs[colorPin] != color:
          print 'connected ' + colorNames[color] + ' to port ' + str(colorPin)
          plugs[colorPin] = color
      else:
        for plug in range(len(plugs)):
          if plugs[plug] == color:
            print 'disconnected ' + colorNames[color] + ' from port ' + str(plug)
            plugs[plug] = None
      sleep(POLL_RATE)

finally: GPIO.cleanup()
