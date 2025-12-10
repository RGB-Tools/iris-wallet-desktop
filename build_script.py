"""
This module handles the build process for the Iris Wallet, including different
platform builds, network settings, and saving build information.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import threading
import time

from src.utils.build_helpers import add_network_argument
from src.utils.build_helpers import apply_app_name_suffix_to_constants
from src.version import __version__

CONSTANT_PATH = os.path.join('src', 'utils', 'constant.py')
TEMP_CONSTANT_PATH = os.path.join('src', 'temp_build_constant.py')


def parse_arguments():
    """Parse command-line arguments for the build script."""
    parser = argparse.ArgumentParser(
        description='Build Iris Wallet for a specified network and distribution.',
    )

    add_network_argument(parser)

    parser.add_argument(
        '--ldk-port',
        required=False,
        help='Specify the LDK Port (Optional).',
    )
    parser.add_argument(
        '--app-name',
        required=False,
        help='Specify the app name to run multiple instances (Optional).',
    )

    if platform.system() == 'Linux':
        # Define the --distribution argument with a help message
        parser.add_argument(
            '--distribution',
            choices=['appimage', 'deb'],
            required=True,
            help="Specify the Linux distribution type: 'appimage' or 'deb'.",
        )

    return parser.parse_args()


def modify_constant_file(app_name: str | None):
    """Modify constant.py to include the app name as a suffix."""
    if not app_name:
        return  # Skip modification if no app name provided

    # Create a temporary copy of the constant file
    shutil.copy(CONSTANT_PATH, TEMP_CONSTANT_PATH)

    with open(CONSTANT_PATH, encoding='utf-8') as file:
        lines = file.readlines()

    suffix = f"_{app_name}"
    new_lines = apply_app_name_suffix_to_constants(lines, suffix)

    # Write modified content back to the file
    with open(CONSTANT_PATH, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def restore_constant_file():
    """Restore the original constant.py from the temporary copy."""
    if os.path.exists(TEMP_CONSTANT_PATH):
        shutil.move(TEMP_CONSTANT_PATH, CONSTANT_PATH)


def loading_animation(stop_event):
    """Simple loading spinner."""
    spinner = '|/-\\'
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(
            f"\rBuild process started, please wait... {
                spinner[idx % len(spinner)]
            }",
        )
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)


def save_build_info_to_json(args, machine_arch, os_type, arch_type):
    """Save the build information to a JSON file."""
    build_info = {
        'build_flavour': args.network,
        'machine_arch': machine_arch,
        'os_type': os_type,
        'arch_type': arch_type,
        'app-version': __version__,
    }

    if os_type == 'Linux':
        build_info['distribution'] = args.distribution

    with open('build_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(build_info, json_file, indent=4)

    print('\nBuild information saved to build_info.json')


def save_app_config(network: str, ldk_port: int | None = None, app_name: str | None = None):
    """Save the network, port, and app name suffix settings to a Python file."""
    flavour_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'src', 'flavour.py',
    )

    # If the file doesn't exist, create it with initial values.
    if not os.path.exists(flavour_file):
        with open(flavour_file, 'w', encoding='utf-8') as file:
            file.write(f"__network__ = '{network}'\n")
            file.write(
                f"__ldk_port__ = '{
                    ldk_port
                }'\n"
                if ldk_port else '__ldk_port__ = None\n',
            )
            file.write(
                f"__app_name_suffix__ = '{
                    app_name
                }'\n"
                if app_name else '__app_name_suffix__ = None\n',
            )
            file.write('__port__ = None\n')
        return

    # If the file exists, read its contents and modify as needed.
    with open(flavour_file, encoding='utf-8') as file:
        lines = file.readlines()

    # Create a new list of lines with updated values.
    new_lines = []
    for line in lines:
        if line.startswith('__network__'):
            new_lines.append(f"__network__ = '{network}'\n")
        elif line.startswith('__ldk_port__'):
            new_lines.append(
                f"__ldk_port__ = '{
                    ldk_port
                }'\n"
                if ldk_port else '__ldk_port__ = None\n',
            )
        elif line.startswith('__app_name_suffix__'):
            new_lines.append(
                f"__app_name_suffix__ = '{
                    app_name
                }'\n"
                if app_name else '__app_name_suffix__ = None\n',
            )
        else:
            new_lines.append(line)

    # Write the modified lines back to the file.
    with open(flavour_file, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def reset_app_config_on_exit():
    """Ensure __port__ and __app_name__ are set to None on exit or Ctrl+C."""
    save_app_config('regtest', None, None)


def main():
    """Main function to handle the build process."""
    args = parse_arguments()
    os_type = platform.system()
    machine_arch = platform.machine()
    arch_type = platform.architecture()[0]

    print('\n\nBuild Summary:')
    if args.app_name:
        print(f"App Name: {args.app_name}")
    print(f"Build Type: {args.network}")
    if args.ldk_port:
        print(f"LDK Port: {args.ldk_port}")
    print(f"Machine Architecture: {machine_arch}")
    print(f"OS Type: {os_type}")
    print(f"Architecture Type: {arch_type}")
    if os_type == 'Linux':
        print(f"Distribution: {args.distribution}")

    result = None
    try:
        modify_constant_file(args.app_name)
        save_build_info_to_json(args, machine_arch, os_type, arch_type)
        save_app_config(args.network, args.ldk_port, args.app_name)

        stop_event = threading.Event()
        loading_thread = threading.Thread(
            target=loading_animation, args=(stop_event,),
        )
        loading_thread.start()

        if os_type == 'Linux':
            if args.distribution == 'appimage':
                result = subprocess.run(
                    ['bash', 'build_appimage.sh'], capture_output=True, text=True, check=True,
                )
            else:
                result = subprocess.run(
                    ['bash', 'build_linux.sh'], capture_output=True, text=True, check=True,
                )
        elif os_type == 'Windows':
            result = subprocess.run(
                ['pyinstaller', 'iris_wallet_desktop.spec'], capture_output=True, text=True, check=True,
            )
        elif os_type == 'Darwin':
            result = subprocess.run(
                ['bash', 'build_macos.sh'], capture_output=True, text=True, check=True,
            )
    finally:
        stop_event.set()
        loading_thread.join()
        restore_constant_file()
        reset_app_config_on_exit()

    if result is not None:
        print('\nOutput:', result.stdout)
        print('Error:', result.stderr)
        print('Return Code:', result.returncode)

        if result.stderr and result.returncode != 0:
            os.remove('build_info.json')


if __name__ == '__main__':
    main()
