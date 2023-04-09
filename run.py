import os
import sys

os.system("source venv/bin/activate")

# collection of all commands that execute on the code
running_cmd = "sudo python main.py"
calibration_cmd = "python CameraLaneDetection/calibrate.py"
add_cmd = "git add ."
commit_cmd = 'git commit -m "saved Calibration/parameters"'
push_cmd = "git push"

# Use this toold to calibrate the camera so it sees the tape
# So far, green colored tape has been used
if "-calibrate" in sys.argv:
    os.system(calibration_cmd)
    exit()

# use this command to push all calibration data to github
# Git directory would need to be set up with remote repo
# in order for it to work
# Once this is called, call git pull on other rc cars
if "-save" in sys.argv:
    os.system(add_cmd)
    os.system(commit_cmd)
    os.system(push_cmd)
    exit()

# this is used to calibrate the PID
if "-testPID" in sys.argv:
    os.system(running_cmd+" -testPID")
else:
    os.system(running_cmd)