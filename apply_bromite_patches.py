#!/usr/bin/env python3

'''
This script will apply patches from bromite to a chromium/src checkout
It wll also configure the output directory with the specified args
'''

import os
import argparse
import subprocess
from subprocess import PIPE
import shutil
from _load_vars import load_vars

# Parse args
args = load_vars(argparse.ArgumentParser(
    description='Configure chromium directory with bromite checkout and patches'
))

chromium = args["chromium"]
bromite = args["bromite"]
root = args["root"]
build_name = args["build_name"]
build_path = args["build_path"]
depot_tools = args["depot_tools"]
env = args["env"]

bromite_build_folder = os.path.join(bromite, 'build')

# Checkout version from RELEASE (or RELEASE_COMMIT?)
print("Checkout chromium version")
release_file_name = os.path.join(bromite_build_folder, 'RELEASE_COMMIT')

with open(release_file_name, 'r', encoding='utf8') as release_file:
    checkout_value = release_file.read()
    print("Checking if commit already downloaded")
    to_exec = f"git cat-file -t {checkout_value}"
    result = subprocess.run(
        to_exec, cwd=chromium,
        shell=True, check=False, env=env,
        stderr=PIPE, stdout=PIPE, encoding="utf8")
    has_commit = "commit" in result.stdout

    if has_commit:
        print("Commit already downloaded")
    else:
        print(f"Fetching release commit {checkout_value}")
        to_exec = f"git fetch --depth=1 origin {checkout_value}"
        subprocess.run(to_exec, cwd=chromium, shell=True, check=True, env=env)
    print(f"Checking out: {checkout_value}")
    to_exec = f"git checkout {checkout_value}"
    subprocess.run(to_exec, cwd=chromium, shell=True, check=True, env=env)

    if not has_commit:
        out_folder = os.path.join(chromium, build_path)
        if os.path.exists(out_folder):
            print("Looks like first time checking out, syncing build tools")
            subprocess.run('gclient sync -D', cwd=chromium, shell=True, check=True, env=env)

# Copy build/bromite.gn_args to out/Default/args.gn (configurable?) (check if exists?)
destination_gn_args = os.path.join(chromium, build_path, 'args.gn')
if os.path.exists(destination_gn_args):
    print("Copy bromite gn args")
    source_gn_args = os.path.join(bromite_build_folder, 'bromite.gn_args')
    shutil.copyfile(source_gn_args, destination_gn_args)
else:
    print("Skipping args.gn since build folder was not initialized")

print("Loading excluded patches list")
PATCHES_TO_SKIP = ""
patch_skip_list_file_name = os.path.join(root, "excluded_patches.txt")
with open(patch_skip_list_file_name, 'r', encoding="utf8") as patch_skip_file:
    PATCHES_TO_SKIP = patch_skip_file.read()

# Get `bromite/build/bromite_patches_list.txt` and read each line
# Skip patches identified in "excluded_patches.txt"
print("Applying patches")
patch_list_file_name = os.path.join(
    bromite_build_folder, 'bromite_patches_list.txt')
with open(patch_list_file_name, 'r', encoding='utf8') as patch_list:
    for patch_name_raw in patch_list:
        patch_name = patch_name_raw.strip()

        if patch_name in PATCHES_TO_SKIP:
            print(f"Skipping: {patch_name}")
            continue

        raw_patch_path = os.path.join(
            bromite_build_folder, 'patches', patch_name.strip())
        patch_path = os.path.abspath(raw_patch_path)

        # Use `git am` to apply patches one by one from `bromite/build/patches/`
        subprocess.run(f"git am {patch_path}",
                       cwd=chromium, shell=True, check=True)

print("Done!")
