import os
import sys

os.system("source venv/bin/activate")

running_cmd = "sudo python main.py"
if "-testPID" in sys.argv:
    os.system(running_cmd+" -testPID")
else:
    os.system(running_cmd)