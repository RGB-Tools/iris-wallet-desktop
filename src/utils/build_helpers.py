"""Shared helpers for build and bootstrap scripts to avoid duplication."""
from __future__ import annotations

from argparse import ArgumentParser
from typing import Iterable


CONSTANT_KEYS_WITH_SUFFIX = (
    'ORGANIZATION_NAME',
    'APP_NAME',
    'ORGANIZATION_DOMAIN',
    'MNEMONIC_KEY',
    'WALLET_PASSWORD_KEY',
    'NATIVE_LOGIN_ENABLED',
    'IS_NATIVE_AUTHENTICATION_ENABLED',
)


def add_network_argument(parser: ArgumentParser) -> None:
    """Add the common --network argument to an ArgumentParser."""
    parser.add_argument(
        '--network',
        choices=['mainnet', 'testnet', 'regtest'],
        required=True,
        help="Specify the network to build for: 'mainnet', 'testnet', or 'regtest'.",
    )


def apply_app_name_suffix_to_constants(lines: Iterable[str], suffix: str) -> list[str]:
    """Return new constants file lines with app-name suffix applied to selected keys."""
    new_lines: list[str] = []
    for line in lines:
        if line.strip().startswith(CONSTANT_KEYS_WITH_SUFFIX):
            key, value = line.split(' = ')
            new_lines.append(f"{key} = {value.strip()[:-1]}{suffix}'\n")
        else:
            new_lines.append(line)
    return new_lines
