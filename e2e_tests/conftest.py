# pylint: disable=redefined-outer-name
"""
Custom pytest configuration for wallet mode testing
"""
from __future__ import annotations

import os
import subprocess
import time

import pytest
from dogtail.tree import root

from accessible_constant import DEFAULT_WALLET_MODES
from src.model.enums.enums_model import WalletType

# Constants for formatting
BANNER_WIDTH = 80
BANNER_SEPARATOR = '=' * BANNER_WIDTH
ERROR_PREVIEW_LENGTH = 200

# Timing constants
CI_STABILIZATION_DELAY = 2.0
LOCAL_STABILIZATION_DELAY = 0.5


def _print_banner(emoji: str, message: str, test_name: str = '') -> None:
    """
    Print a formatted banner for test events.

    Args:
        emoji: Emoji to display
        message: Message to display
        test_name: Optional test name to append
    """
    full_message = f"{message}: {test_name}" if test_name else message
    print(f"\n{BANNER_SEPARATOR}")
    print(f"{emoji} {full_message}")
    print(f"{BANNER_SEPARATOR}\n")


def _print_test_result(status_emoji: str, status: str, test_name: str, error_text: str = '') -> None:
    """
    Print a test result message.

    Args:
        status_emoji: Emoji representing the status
        status: Status text (PASSED, FAILED, SKIPPED)
        test_name: Name of the test
        error_text: Optional error message for failed tests
    """
    print(f"{status_emoji} {status}: {test_name}")
    if error_text:
        print(f"   Error: {error_text[:ERROR_PREVIEW_LENGTH]}...")


def pytest_addoption(parser):
    """
    Add custom command-line options for pytest to select wallet mode.

    :param parser: pytest parser object
    """
    parser.addoption(
        '--wallet-mode',
        action='store',
        choices=DEFAULT_WALLET_MODES,
        help="Set wallet mode to 'embedded' or 'remote'. If not provided, tests run for both modes.",
    )


def pytest_generate_tests(metafunc):
    """
    Dynamically run tests for both wallet modes if --wallet-mode is not provided.

    :param metafunc: pytest metafunction object
    """
    if 'wallet_mode' in metafunc.fixturenames:
        wallet_mode = metafunc.config.getoption('wallet_mode')
        if wallet_mode:
            # Run for the specified mode
            metafunc.parametrize('wallet_mode', [wallet_mode])
        else:
            # Run for both modes
            metafunc.parametrize('wallet_mode', DEFAULT_WALLET_MODES)


@pytest.fixture(scope='session')
def wallet_mode(request):
    """
    Fixture to provide the selected wallet mode.

    :param request: Pytest request object
    :return: selected wallet mode
    """
    return request.param


def pytest_runtest_setup(item):
    """Skip tests based on wallet mode and print test start."""
    # Print test start banner
    _print_banner('🧪', 'STARTING TEST', item.nodeid)

    wallet_mode = item.config.getoption('--wallet-mode')

    # Skip tests marked with @pytest.mark.skip_for_embedded if running in embedded mode
    if wallet_mode == WalletType.EMBEDDED_TYPE_WALLET.value and any(mark.name == 'skip_for_embedded' for mark in item.own_markers):
        pytest.skip(
            'Skipping test because it is not applicable in embedded mode.',
        )

    # Skip tests marked with @pytest.mark.skip_for_remote if running in remote mode
    if wallet_mode == WalletType.REMOTE_TYPE_WALLET.value and any(mark.name == 'skip_for_remote' for mark in item.own_markers):
        pytest.skip(
            'Skipping test because it is not applicable in remote mode.',
        )


def pytest_runtest_teardown(item):
    """Print test completion banner."""
    _print_banner('✅', 'COMPLETED TEST', item.nodeid)


def pytest_runtest_logreport(report):
    """Print test result after execution."""
    if report.when == 'call':
        test_name = report.nodeid
        if report.passed:
            _print_test_result('✅', 'PASSED', test_name)
        elif report.failed:
            _print_test_result('❌', 'FAILED', test_name, report.longreprtext)
        elif report.skipped:
            _print_test_result('⏭️', 'SKIPPED', test_name)


def _is_ci_environment():
    """Check if running in CI environment."""
    return os.getenv('CI', '').lower() in ('true', '1', 'yes')


def _refresh_atspi_tree():
    """
    Force AT-SPI tree refresh by accessing root.
    This helps clear stale element caches between tests.
    """
    try:
        _ = root.children
    except Exception:
        pass


def _reset_operations_state(test_environment):
    """
    Reset state in all BaseOperations instances.
    Clears debounce tracking, circuit breakers, and window switch flags.
    """
    try:
        if hasattr(test_environment, 'first_page_operations'):
            test_environment.first_page_operations.reset_state()

        if test_environment.multi_instance and hasattr(test_environment, 'second_page_operations'):
            test_environment.second_page_operations.reset_state()
    except Exception:
        pass


def _stabilize_ui(delay_seconds):
    """
    Add stabilization delay for UI and AT-SPI to settle.
    Longer delays in CI to account for slower accessibility tree synchronization.
    """
    time.sleep(delay_seconds)


def _verify_no_zombie_processes():
    """
    Check for any zombie AppImage or RGB processes.
    Note: Module-scoped fixtures keep main processes alive.
    """
    try:
        subprocess.run(
            ['pgrep', '-f', 'iriswallet.*AppImage'],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        pass


@pytest.fixture(autouse=True)
def cleanup_between_tests(request):
    """
    Automatic cleanup fixture that runs between each test function.

    This fixture ensures clean state when using module-scoped test_environment
    by:
    - Yielding before the test runs
    - Performing cleanup after the test completes
    - Refreshing AT-SPI tree to clear stale caches
    - Resetting all BaseOperations state
    - Adding stabilization delays in CI

    The fixture only runs when test_environment is available (scope='module').
    """
    # Before test: nothing to do
    yield

    # After test: perform cleanup
    try:
        # Get the test_environment fixture if it exists
        if 'test_environment' in request.fixturenames:
            test_env = request.getfixturevalue('test_environment')

            _print_banner('🧹', 'CLEANUP', 'Running inter-test cleanup')

            # 1. Refresh AT-SPI tree to clear stale element caches
            _refresh_atspi_tree()

            # 2. Reset state in BaseOperations instances
            _reset_operations_state(test_env)

            # Stabilization delay (longer in CI)
            delay = CI_STABILIZATION_DELAY if _is_ci_environment() else LOCAL_STABILIZATION_DELAY
            _stabilize_ui(delay)

            # 4. Verify no zombie processes
            _verify_no_zombie_processes()

            _print_banner('✅', 'CLEANUP', 'Complete')
    except Exception as e:
        # Don't fail tests if cleanup has issues
        print(f'[CLEANUP] Warning: Cleanup encountered an error: {e}')
