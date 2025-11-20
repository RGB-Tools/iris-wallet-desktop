# pylint: disable=redefined-outer-name
"""
This module help to run any pre-execution tasks

Use :
====
Just define any function and call it immediately, or anything else, and it will run before main.py executes.
"""
from __future__ import annotations

import argparse
import atexit
import shutil
import sys
from pathlib import Path

import src.flavour as bitcoin_network
from build_script import CONSTANT_PATH
from build_script import TEMP_CONSTANT_PATH
from src.utils.build_helpers import add_network_argument
from src.utils.build_helpers import apply_app_name_suffix_to_constants


def network_configure():
    """Parse the arguments and configure network (only in case of command line execution not build)"""
    parser = argparse.ArgumentParser(
        description='Run Iris Wallet for a specified network and distribution.',
    )

    # Define the --network argument with a help message
    add_network_argument(parser)

    # Add the --app-name argument
    parser.add_argument(
        '--app-name',
        required=False,
        help='Specify the app name to run multiple instances (Optional).',
    )

    # Parse the arguments
    args = parser.parse_args()

    # Set the network for the Bitcoin network module
    bitcoin_network.__network__ = args.network

    # Return the parsed arguments so that they can be used elsewhere
    return args


def modify_constant_file(app_name: str | None):
    """
    Modify constant.py to include the app name as a suffix or restore it to the original state
    if no app name is provided.
    """
    temp_path = Path(TEMP_CONSTANT_PATH)

    # Restore the original constants file if no app name is provided
    if not app_name:
        if temp_path.exists():
            shutil.copy(temp_path, CONSTANT_PATH)
        return

    # Create a backup of the constants file if it doesn't already exist
    if not temp_path.exists():
        shutil.copy(CONSTANT_PATH, TEMP_CONSTANT_PATH)

    # Read the current constants file
    with open(TEMP_CONSTANT_PATH, encoding='utf-8') as backup_file:
        original_lines = backup_file.readlines()

    with open(CONSTANT_PATH, encoding='utf-8') as current_file:
        current_lines = current_file.readlines()

    # Detect if app name was already added (to prevent duplicate app name suffixes)
    suffix = f"_{app_name}"
    if any(suffix in line for line in current_lines):
        return

    # Modify the constants file by appending the app name suffix
    new_lines = apply_app_name_suffix_to_constants(original_lines, suffix)

    # Write the modified content back to the constants file
    with open(CONSTANT_PATH, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def restore_constant_file():
    """Restore the original constant file and remove the temporary backup."""
    temp_path = Path(TEMP_CONSTANT_PATH)
    if temp_path.exists():
        shutil.copy(temp_path, CONSTANT_PATH)  # Restore original constants
        temp_path.unlink()  # Delete the temporary backup file


# Dev note: Exercise caution before removing this section of code.
if not getattr(sys, 'frozen', False):
    args = network_configure()
    # Use the app-name argument in modify_constant_file
    modify_constant_file(args.app_name)
    atexit.register(restore_constant_file)
