#!/usr/bin/env python3

'''
This script will trigger a new build of the browser
'''

import os
import argparse
import requests

from _load_vars import load_vars

parser = argparse.ArgumentParser(
    description='Download the IPFS daemon AAR file'
)

# TODO: Use specific tag once we have a stable release
DEFAULT_VERSION = "latest"
DEFAULT_REPO = 'AgregoreWeb/agregore-ipfs-daemon'
DEFAULT_BINARY_NAME = 'agregore-ipfs-daemon.aar'

parser.add_argument(
    '--version',
    default=DEFAULT_VERSION,
    help="What version tag to use for the gateway"
)

parser.add_argument(
    '--repo',
    default=DEFAULT_REPO,
    help="Name of the github repo to download from"
)

parser.add_argument(
    '--binary_name',
    default=DEFAULT_BINARY_NAME,
    help="Name of the aar file to download from the release"
)

args = load_vars(parser)

chromium = args["chromium"]
env = args["env"]

version = args["version"]
repo = args["repo"]
binary_name = args["binary_name"]

url = f"https://github.com/{repo}/releases/{version}/download/{binary_name}"

print(f"Downloading {url}")

response = requests.get(url, allow_redirects=True, stream=True)

download_location = os.path.join(
    chromium,
    "third_party/agregore-ipfs-daemon/agregore-ipfs-daemon.aar"
)

with open(download_location, 'wb') as file:
    file.write(response.content)

print("Done!")
