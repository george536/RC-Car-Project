import os
import sys

os.system("source venv/bin/activate")

running_cmd = "sudo python main.py"
calibration_cmd = "python CameraLaneDetection/calibrate.py"
add_cmd = "git add ."
commit_cmd = 'git commit -m "saved Calibration/parameters"'
push_cmd = "git push"

if "-calibrate" in sys.argv:
    os.system(calibration_cmd)
    exit

if "-save" in sys.argv:
    os.system(add_cmd)
    os.system(commit_cmd)
    os.system(push_cmd)
    exit

if "-testPID" in sys.argv:
    os.system(running_cmd+" -testPID")
else:
    os.system(running_cmd)