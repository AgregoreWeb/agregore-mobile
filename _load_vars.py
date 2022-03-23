#!/usr/bin/env python3

'''
This script will parse arguments for configuring scripts
'''

import os
import argparse

CURRENT_FOLDER = os.path.dirname(__file__)
DEFAULT_BROMITE = os.path.abspath(os.path.join(CURRENT_FOLDER, './bromite'))
DEFAULT_CHROMIUM = os.path.abspath(os.path.join(CURRENT_FOLDER, './chromium/src'))
DEFAULT_DEPOT_TOOLS = os.path.abspath(os.path.join(CURRENT_FOLDER, './depot_tools'))


def load_vars(existing_parser=None):
    """
    This function will load common CLI arguments
    You can optionally specify an existing argparse parser
    """
    if existing_parser is not None:
        parser = existing_parser
    else:
        parser = argparse.ArgumentParser(
            description='Load variables'
        )

    parser.add_argument(
        '--depot_tools',
        default=DEFAULT_DEPOT_TOOLS,
        help="The folder for chrome depot_tools"
    )
    parser.add_argument(
        '--bromite',
        default=DEFAULT_BROMITE,
        help="The bromite folder to get patches from"
    )
    parser.add_argument(
        '--chromium',
        default=DEFAULT_CHROMIUM,
        help="The chromium/src folder to do builds within"
    )
    parser.add_argument(
        '--build_name',
        default="Default",
        help="The name within the chromium/src/out folder to use for the build"
    )

    args = parser.parse_args()

    arg_dict = vars(args)

    chromium = args.chromium
    chromium_root = os.path.abspath(os.path.join(chromium, "../"))

    build_name = args.build_name
    build_path = "out/" + build_name

    bromite = args.bromite
    bromite_build_folder = os.path.abspath(os.path.join(bromite, 'build'))

    final_args = dict(arg_dict, **{
        "chromium_root": chromium_root,
        "bromite_build_folder": bromite_build_folder,
        "build_path": build_path,
        "root": CURRENT_FOLDER
    })

    return final_args
