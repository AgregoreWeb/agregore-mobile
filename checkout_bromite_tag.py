#!/usr/bin/env python3

'''
This script will checkout the version of bromite specified in bromite_tag.txt
'''

import os
import subprocess
import argparse

from _load_vars import load_vars

parser = argparse.ArgumentParser(
    description='Checkout the version of bromite specified in bromite_tag.txt'
)

bromite_tag_file_path = os.path.normpath(os.path.join(
    os.path.realpath(__file__),
    "../bromite_tag.txt"
))

DEFAULT_VERSION = ""

with open(bromite_tag_file_path, "r", encoding="utf8") as bromite_tag_file:
    DEFAULT_VERSION = bromite_tag_file.read().strip()

parser.add_argument(
    '--version',
    default=DEFAULT_VERSION,
    help="What version tag to use for bromite"
)

args = load_vars(parser)

env = args["env"]
bromite = args["bromite"]

version = args["version"]

print(f"Checking out bromite version {version}")

to_exec = f"git checkout {version}"
subprocess.run(to_exec, cwd=bromite, shell=True, check=True, env=env)

print("Done!")
