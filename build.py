#!/usr/bin/env python3

'''
This script will trigger a new build of the browser
'''

import os
import argparse
import subprocess

from _load_vars import load_vars

args = load_vars(argparse.ArgumentParser(
    description='Build the browser'
))

chromium = args["chromium"]
build_name = args["build_name"]
build_path = args["build_path"]
depot_tools = args["depot_tools"]

autoninja = os.path.join(depot_tools, 'autoninja')

print(f"Building {build_name}")
to_run = f'{autoninja} -C {build_path} chrome_public_apk'
subprocess.run(to_run, cwd=chromium, shell=True, check=True)

print("Done!")
