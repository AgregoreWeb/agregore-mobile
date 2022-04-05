#!/usr/bin/env python3

'''
This script will undo the last patch
'''

import argparse
import subprocess

from _load_vars import load_vars

args = load_vars(argparse.ArgumentParser(
    description='Undo the last patch'
))

chromium = args["chromium"]
env = args["env"]

print("Undoing last patch")
subprocess.run('git checkout HEAD~1', cwd=chromium,
               shell=True, check=True, env=env)

print("Done!")
