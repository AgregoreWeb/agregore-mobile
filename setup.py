#!/usr/bin/env python3

'''
This script will set up the current folder with its dependencies
'''

import os
import argparse
import subprocess
from _load_vars import load_vars

GN_ARGS = 'target_os = "android"\ntarget_cpu = "arm64"\n'.encode('utf-8')

parser = argparse.ArgumentParser(
    description='Initialize the current directory with dependencies'
)

parser.add_argument(
    '--build',
    action="store_true",
    default=False,
    help="Whether to prepare the source tree for a build"
)

parser.add_argument(
    '--depot_tools_repo',
    default="https://chromium.googlesource.com/chromium/tools/depot_tools.git",
    help="The git repo for chromium build tools"
)

parser.add_argument(
    '--bromite_repo',
    default="https://github.com/bromite/bromite.git",
    help="The git repo for bromite"
)

args = load_vars(parser)

chromium = args["chromium"]
chromium_root = args["chromium_root"]
bromite = args["bromite"]
build_name = args["build_name"]
build_path = args["build_path"]
depot_tools = args["depot_tools"]
root = args["root"]
env = args["env"]

build = args["build"]
depot_tools_repo = args["depot_tools_repo"]
bromite_repo = args["bromite_repo"]

bromite_build_folder = os.path.join(bromite, 'build')

# Set up ./depot_tools if it doesn't exist
if not os.path.exists(depot_tools):
    print('Cloning depot_tools')
    subprocess.run(f'git clone {depot_tools_repo}',
                   cwd=root, shell=True, check=True)
else:
    print("Skipping depot_tools, already exists")
# Set up ./chromium/src if it doesn't exist
if not os.path.exists(chromium_root):
    print("Fetching chromium source")
    os.makedirs(chromium_root)
    subprocess.run('fetch --nohooks android',
                   cwd=chromium_root, shell=True, check=True, env=env)
    if build:
        print('Installing build dependencies')
        install_deps = os.path.join(
            chromium, "build/install-build-deps-android.sh")
        subprocess.run(f'{install_deps}', cwd=chromium_root,
                       shell=True, check=True, env=env)
        print('Running hooks for third party libraries')
        subprocess.run('gclient runhooks',
                       cwd=chromium_root, shell=True, check=True, env=env)
    else:
        print("Skipping build dependencies, enable with --build")
else:
    print("Skipping chromium root, already exists")
# Set up ./chromium/src/out/Default if it doesn't exist
if build and not os.path.exists(os.path.join(chromium, build_path)):
    print('Preparing chromium output directory')
    subprocess.run(
        f'gn args {build_path}',
        input=GN_ARGS, cwd=chromium_root, shell=True, check=True, env=env)
else:
    print("Skipping chromium output directory, exists or not building")
# Set up ./bromite if it doesn't exist
if not os.path.exists(bromite):
    print('Cloning bromite repo')
    subprocess.run(f'git clone {bromite_repo}',
                   cwd=root, shell=True, check=True)
else:
    print("Skipping bromite directory, already exists")

print("Running Bromite Patch Script")
bromite_patch_script = os.path.join(root, 'patch_with_bromite.py')
subprocess.run(bromite_patch_script, cwd=root, shell=True, check=True)

print("Running Agregore Patch Script")
agregore_patch_script = os.path.join(root, 'apply_agregore_patches.py')
subprocess.run(agregore_patch_script, cwd=root, shell=True, check=True)

print("Running Download IPFS Daemon Script")
download_ipfs_daemon_script = os.path.join(root, 'download_ipfs_daemon.py')
subprocess.run(download_ipfs_daemon_script, cwd=root, shell=True, check=True)

print("Really Done!")
