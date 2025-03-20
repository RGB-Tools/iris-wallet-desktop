"""This module is used for executing shell commands to fund the wallet and mine"""
from __future__ import annotations

import subprocess


def execute_shell_command(command):
    """
    Execute a shell command and return the output.

    Args:
        command (str): The command to execute.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    try:
        result = subprocess.run(
            command, shell=True,
            capture_output=True, text=True, check=True,
        )

        return result.stdout

    except subprocess.CalledProcessError as error:
        raise subprocess.CalledProcessError(
            returncode=error.returncode, cmd=error.cmd, output=error.output, stderr=error.stderr,
        )


def send_to_address(address, amount):
    """
    Send bitcoin to an address.

    Args:
        address (str): The address to send to.
        amount (str): The amount to send.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    command = f"bash e2e_tests/regtest.sh sendtoaddress {
        address
    } {amount}"
    return execute_shell_command(command)


def mine(amount):
    """
    Mine bitcoin.

    Args:
        amount (str): The amount to mine.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    command = f"bash e2e_tests/regtest.sh mine {
        amount
    }"
    return execute_shell_command(command)


def get_working_directory():
    """gets the working directory"""

    command = 'pwd'
    return execute_shell_command(command)
