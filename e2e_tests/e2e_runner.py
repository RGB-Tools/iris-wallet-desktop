"""
End-to-End testing script for embedded and remote wallet modes.
"""
from __future__ import annotations

import subprocess
import sys

from accessible_constant import DEFAULT_WALLET_MODES

E2E_SCRIPT = './run_e2e_tests.sh'
# Default modes if none is provided


def run_e2e(extra_args=None):
    """Runs the e2e.sh script with optional arguments."""
    cmd = ['bash', E2E_SCRIPT]
    if extra_args:
        cmd.extend(extra_args)
    subprocess.run(cmd, check=True)


def serve_allure_result(results_dir):
    """Serves the Allure report for a specific results directory."""
    subprocess.run(['allure', 'serve', results_dir], check=True)


def single_test():
    """Runs a single test with an optional wallet mode and force build."""
    if len(sys.argv) < 2:
        print('Usage: single-test <test-file> [wallet-mode] [force build]')
        sys.exit(1)

    test_file = sys.argv[1]
    wallet_mode = None
    force_build = False

    # Parse optional arguments
    for arg in sys.argv[2:]:
        if arg in DEFAULT_WALLET_MODES:
            wallet_mode = arg
        elif arg.lower() == 'force-build':
            force_build = True
        else:
            print(f"Error: Unrecognized argument '{arg}'")
            sys.exit(1)

    if force_build:
        print('Forcing application build before running tests...')
        run_e2e(['--force-build'])

    if wallet_mode:
        run_e2e([test_file, '--wallet-mode', wallet_mode])
    else:
        for mode in DEFAULT_WALLET_MODES:
            print(f"Running test '{test_file}' with wallet mode: {mode}")
            run_e2e([test_file, '--wallet-mode', mode])


def e2e_test():
    """Runs all E2E tests with 'all' (required) and optional wallet mode & force build."""
    force_build = None
    if 'all' not in sys.argv:
        print("Error: The 'all' argument is required for e2e tests.")
        sys.exit(1)

    wallet_mode = None
    extra_args = ['--all']

    # Parse optional arguments
    for arg in sys.argv[1:]:
        if arg in DEFAULT_WALLET_MODES:
            wallet_mode = arg
        elif arg.lower() == 'force-build':
            force_build = True
        elif arg.lower() != 'all':
            print(f"Error: Unrecognized argument '{arg}'")
            sys.exit(1)

    if force_build:
        print('Forcing application build before running tests...')
        run_e2e(['--force-build'])

    if wallet_mode:
        run_e2e(extra_args + ['--wallet-mode', wallet_mode])
    else:
        for mode in DEFAULT_WALLET_MODES:
            print(f"Running full test suite with wallet mode: {mode}")
            run_e2e(extra_args + ['--wallet-mode', mode])


def result_embedded():
    """Serves the allure report for embedded wallet mode."""
    serve_allure_result('allure-results-embedded')


def result_remote():
    """Serves the allure report for remote wallet mode."""
    serve_allure_result('allure-results-remote')


def run_regtest(extra_args=None):
    """Runs the regtest script with optional arguments."""
    cmd = [
        'bash', '-c',
        'COMPOSE_FILE=compose.yaml ./e2e_tests/regtest.sh start',
    ]
    if extra_args:
        cmd.extend(extra_args)
    subprocess.run(cmd, check=True)
