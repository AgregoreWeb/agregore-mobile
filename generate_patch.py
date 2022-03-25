#!/usr/bin/env python3

'''
This script will generate a new patch from the latest commit.
'''

import os
import argparse
import subprocess

from _load_vars import load_vars

parser = argparse.ArgumentParser(
    description='Generate patch from the latest commit'
)

parser.add_argument(
    '--n',
    default="HEAD^",
    help="Number of commits to use for the patch"
)

args = load_vars(parser)

chromium = args["chromium"]
env = args["env"]
root = args["root"]
n = args["n"]

patch_dir = os.path.join(root, 'patches')

print("Generating patch from latest commit")
to_run = f'git format-patch -N {n} -o {patch_dir}'
result = subprocess.run(to_run, cwd=chromium, shell=True,
                        check=True, env=env, encoding="utf8")

patch_name = result.stdout


print("Done!")
