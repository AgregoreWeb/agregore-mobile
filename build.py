#!/usr/bin/env python3

'''
This script will trigger a new build of the browser
'''

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
env = args["env"]

print(f"Building {build_name}")
to_run = f'autoninja -C {build_path} trichrome_chrome_bundle'
subprocess.run(to_run, cwd=chromium, shell=True, check=True, env=env)

print("Done!")
