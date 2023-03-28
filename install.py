import os
commands = [
    'sudo pip install opencv-python',
    'sudo pip install paho-mqtt'
]

for cmd in commands:
    os.system(cmd)