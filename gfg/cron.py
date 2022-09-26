from genericpath import exists
import subprocess
import platform

import os.path
from os import path

str = "macOS-12.4-arm64-arm-64bit"
if platform.platform() == str:
    subprocess.run(
        ["crontab", "-e"]
    )  # paste this on macos - * * * * * /opt/homebrew/bin/python3 /Users/rahulrocksn/Desktop/workspace/scrape/gfg/cron_job.py >> ~/cron.log 2>&1
else:
    print("use a mac peasant(just kidding)")

exist = path.exists(os.path.dirname(__file__) + "/search.txt")
if exist:
    subprocess.run(["python3", "cron_job.py"])
else:
    subprocess.run(["python3", "form.py"])
