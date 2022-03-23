#!/usr/bin/env python3

'''
This script will clean the build folder and ensure that
third partydependenciesare synchronized before doing a build.
'''

import argparse
import subprocess

from _load_vars import load_vars

args = load_vars(argparse.ArgumentParser(
    description='Sync chromium dependencies before performing a build'
))

chromium = args["chromium"]
build_path = args["build_path"]
depot_tools = args["depot_tools"]
env = args["env"]

print("Clean the build folder")
subprocess.run(f'gn clean {build_path}',
               cwd=chromium, shell=True, check=True, env=env)

print("Sync dependencies with gclient")
subprocess.run('gclient sync -D', cwd=chromium,
               shell=True, check=True, env=env)

print("Done!")
