#!/usr/bin/env python3

'''
This script will apply patches from bromite to a chromium/src checkout
It wll also configure the output directory with the specified args
'''

import os
import argparse
import subprocess
from subprocess import PIPE
from _load_vars import load_vars

# Parse args
args = load_vars(argparse.ArgumentParser(
    description='Apply agregore-specific patches'
))

chromium = args["chromium"]
root = args["root"]
env = args["env"]

patch_dir = os.path.join(root, 'patches')
patch_list_file = os.path.join(root, "agregore_patch_order.txt")

print("Applying patches")
with open(patch_list_file, 'r', encoding="utf8") as patch_list:
    for patch_name_raw in patch_list:
        patch_name = patch_name_raw.strip()
        raw_patch_path = os.path.join(patch_dir, patch_name)
        patch_path = os.path.abspath(raw_patch_path)
        result = subprocess.run(
            f"git am {patch_path}",
            cwd=chromium,
            shell=True, check=False,
            stderr=PIPE, encoding="utf8"
        )
        if result.returncode != 0:
            # If the patch was already applied, skip it. 🤷
            if 'patch does not apply' in result.stderr:
                print(f"Patch {patch_name} does not apply, skipping")
                subprocess.run("git am --skip", cwd=chromium,
                               shell=True, check=True)
            else:
                print(result.stderr)
                result.check_returncode()

print("Done!")
