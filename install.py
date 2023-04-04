import os
import time
commands = [
    'sudo pip install smbus',
    'sudo pip install RPi.GPIO',
    'sudo pip install rpi_ws281x',
    'sudo pip install paho-mqtt'
    'sudo pip install opencv-python',
    'sudo pip install picamera2',
    'sudo pip install libcamera',
]

for cmd in commands:
    os.system(cmd)
    time.sleep(0.5)