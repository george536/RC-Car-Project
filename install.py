import os
import time
commands = [
    'sudo pip install smbus',
    'sudo pip install RPi.GPIO',
    'sudo pip install rpi_ws281x',
    'sudo pip install paho-mqtt',
    'sudo pip install opencv-python',
    'sudo pip install picamera2',
    'sudo apt install -y python3-picamera2',
    'sudo apt-get install build-essential libcap-dev'
]

for cmd in commands:
    os.system(cmd)
    time.sleep(0.5)