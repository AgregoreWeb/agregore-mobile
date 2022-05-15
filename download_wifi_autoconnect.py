#!/usr/bin/env python3

'''
This script will trigger a new build of the browser
'''

import os
import argparse
import requests

from _load_vars import load_vars

parser = argparse.ArgumentParser(
    description='Download the WifiAutoConnect AAR file'
)

tag_file_path = os.path.normpath(os.path.join(
    os.path.realpath(__file__),
    "../wifi_auto_connect_tag.txt"
))

DEFAULT_VERSION = ""

with open(tag_file_path, "r", encoding="utf8") as tag_file:
    DEFAULT_VERSION = tag_file.read().strip()

DEFAULT_REPO = 'RangerMauve/WifiAutoConnect-Android'
DEFAULT_BINARY_NAME = 'WifiAutoConnect.aar'

parser.add_argument(
    '--version',
    default=DEFAULT_VERSION,
    help="What version tag to use for the library"
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

url = f"https://github.com/{repo}/releases/download/{version}/{binary_name}"

# TODO: Reuse script for downloading

print(f"Downloading {url}")

response = requests.get(url, allow_redirects=True, stream=True)

# Raise an exception if we get a 404
response.raise_for_status()

download_location = os.path.join(
    chromium,
    "third_party/wifi_autoconnect/WifiAutoConnect.aar"
)

with open(download_location, 'wb') as file:
    file.write(response.content)

print("Done!")
